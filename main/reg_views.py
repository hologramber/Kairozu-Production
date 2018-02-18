from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from main.models import Chapter, Lesson, Profile
from main.forms import SignUpForm, ChangeStrictModeForm
from main.tokens import activationtoken


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            subject = 'Activate Your Kairozu Account'
            message = render_to_string('email/activation_email.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                #'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': activationtoken.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def activation_sent(request):
    return render(request, 'email/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        #uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and activationtoken.check_token(user, token):
        user.is_active = True
        user.profile.emailconfirmed = True
        user.save()
        login(request, user)
        return redirect('newuser')
    else:
        return render(request, 'email/activation_invalid.html')


def newuser(request):
    return render(request, 'account_newuser.html')


def account(request):
    currentchapter = get_object_or_404(Chapter, pk=request.user.profile.currentchapter)
    currentlesson = get_object_or_404(Lesson, pk=request.user.profile.currentlesson)
    if 'passchange' in request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request, messages.SUCCESS, 'Your password was successfully updated!')
            return redirect('account')
        else:
            messages.error(request, 'Please correct the error below.')
    elif 'strictchange' in request.POST:
        userprofile = Profile.objects.get(user_id__exact=request.user.id)
        strictform = ChangeStrictModeForm(request.POST, instance=userprofile)
        if strictform.is_valid():
            strictform.save()
            messages.add_message(request, messages.SUCCESS, 'Your settings have been updated.')
            return redirect('account')
        else:
            messages.add_message(request, messages.ERROR, 'Settings have not been updated. Contact kairozu@kairozu.com for help.')
    else:
        form = PasswordChangeForm(request.user)
        strictdata = {'strictmode': request.user.profile.strictmode}
        strictform = ChangeStrictModeForm(strictdata)
    return render(request, 'account.html', {'form': form, 'strictform': strictform, 'currentchapter': currentchapter, 'currentlesson': currentlesson})


def error_404(request):
    data = {}
    return render(request, '404.html', data)


def error_500(request):
    data = {}
    return render(request, '500.html', data)
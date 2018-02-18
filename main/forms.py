from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ChangeStrictModeForm(forms.ModelForm):
    strictmode = forms.BooleanField(label='Strict Mode', help_text='<ul><li>Force exact matching on word order when evaluating practice and quiz sentences.</li></ul>', required=False)

    class Meta:
        model = Profile
        fields = ('strictmode',)

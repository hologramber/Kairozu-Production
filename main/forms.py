from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import Profile, Flashcard


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ChangeStrictModeForm(forms.ModelForm):
    strictmode = forms.BooleanField(label='Strict Mode', help_text='<ul><li>Force exact matching on word order when evaluating practice and quiz sentences.</li></ul>', required=False)
    preferkanji = forms.BooleanField(label='Prefer Kanji', help_text='<ul><li>Display hints in kanji and accept kanji input when appropriate.</li></ul>', required=False)

    class Meta:
        model = Profile
        fields = ('strictmode', 'preferkanji')


class ValidateFinishForm(forms.Form):
    q = forms.IntegerField(max_value=50)
    totalq = forms.IntegerField(max_value=50)


class ValidateExerciseFinish(forms.Form):
    q = forms.IntegerField(max_value=50)
    totalq = forms.IntegerField(max_value=50)
    score = forms.FloatField(max_value=1.1)


class FlashcardForm(forms.ModelForm):
    strict = forms.BooleanField(label='Strict Mode', help_text='Force exact matching on word & character order.')
    literal = forms.CharField(label='Literal Meaning', help_text='Literal translation between English and Japanese.', required=False)
    context = forms.CharField(help_text='Additional context, e.g. speech used in a formal setting.', required=False)
    note = forms.CharField(help_text='Other information or additional notes regarding this flashcard.', required=False)
    kanji = forms.CharField(required=False)
    class Meta:
        model = Flashcard
        fields = ['english', 'kana', 'kanji', 'strict', 'literal', 'context', 'note']
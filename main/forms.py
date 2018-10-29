from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import Profile, Flashcard, FlashcardSet, BetaEmail

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


class EmailBetaForm(forms.ModelForm):
    user_beta_email = forms.EmailField(label="", max_length=50)

    class Meta:
        model = BetaEmail
        exclude = ('user_beta_submitted',)


class FlashcardForm(forms.ModelForm):
    strict = forms.BooleanField(label='Strict Mode', help_text='Force exact matching on word & character order.', required=False)
    literal = forms.CharField(label='Literal Meaning', help_text='Literal translation between English and Japanese.', required=False)
    context = forms.CharField(help_text='Additional context, e.g. speech used in a formal setting.', required=False)
    note = forms.CharField(required=False)
    kanji = forms.CharField(required=False)

    class Meta:
        model = Flashcard
        fields = ['english', 'set', 'kana', 'kanji', 'strict', 'literal', 'context', 'note']


class FlashcardSetForm(forms.ModelForm):
    name = forms.CharField(label='Flashcard set name', help_text='10 character limit; must be unique!', required=True)
    description = forms.CharField(help_text='Additional description for this set of flashcards.', required=False)

    class Meta:
        model = FlashcardSet
        fields = ['name', 'description']
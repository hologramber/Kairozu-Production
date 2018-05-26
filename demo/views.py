from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.urls import reverse
from main.models import Lesson
from .models import DemoVocab, DemoExpression, BetaEmail
from .forms import EmailBetaForm


def demointerface(request):
    return render(request, 'demo/interface.html')


def demointro(request):
    return render(request, 'demo/introduction.html')


class GrammarListView(ListView):
    context_object_name = 'grammar_list'
    queryset = Lesson.objects.filter(id__lte=40)
    template_name = 'demo/grammarlist.html'


def storydemo(request):
    return render(request, 'demo/storydemo.html')


def dialoguedemo(request):
    return render(request, 'demo/dialoguedemo.html')


def demokana(request):
    return render(request, 'demo/demokana.html')


class DemoVocabListView(ListView):
    model = DemoVocab
    template_name = 'demo/vocablist.html'


class DemoVocabQuizView(TemplateView):
    template_name = 'demo/vocabquiz.html'


class DemoVocabSuccessView(TemplateView):
    template_name = 'demo/vocabsuccess.html'


class DemoExpressionListView(ListView):
    model = DemoExpression
    template_name = 'demo/expressionlist.html'


class DemoExpressionQuizView(TemplateView):
    template_name = 'demo/expressionquiz.html'


class DemoExpressionSuccessView(TemplateView):
    template_name = 'demo/expressionsuccess.html'


def demolesson(request):
    return render(request, 'demo/examplelesson.html')


class DemoPracticeQuizView(TemplateView):
    template_name = 'demo/practicequiz.html'


class DemoPracticeSuccessView(TemplateView):
    template_name = 'demo/practicesuccess.html'


class DemoSentenceQuizView(TemplateView):
    template_name = 'demo/sentencequiz.html'


class DemoSentenceSuccessView(TemplateView):
    template_name = 'demo/sentencesuccess.html'


class BetaEmailView(CreateView):
    template_name = 'closed_register.html'
    form_class = EmailBetaForm

    def get_success_url(self):
        return reverse('betaconfirm')


class BetaConfirmView(TemplateView):
    template_name = 'closed_success.html'
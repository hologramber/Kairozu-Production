from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse
from .models import Sandcastle
from .num2jp_kana import num2jp_kana
import json


class SandboxView(ListView):
    model = Sandcastle
    template_name = 'sandbox/index.html'

    def get_context_data(self, **kwargs):
        context = super(SandboxView, self).get_context_data(**kwargs)
        return context


def japanesekana(request):
    return render(request, 'sandbox/japanesekana.html')


def joshi(request):
    return render(request, 'sandbox/joshi.html')


def kaimono(request):
    return render(request, 'sandbox/kaimono.html')


def katakana(request):
    return render(request, 'sandbox/katakana.html')


def hiragana(request):
    return render(request, 'sandbox/hiragana.html')


class NumberQuizView(TemplateView):
    template_name = 'sandbox/numberquiz.html'


def numquiz_grab(request):
    if request.POST:
        max_num = int(request.POST['max_number'])
    else:
        max_num = 99
    num_digits, num_kana = num2jp_kana(1, max_num)
    data = {'numd': "{:,}".format(num_digits), 'numk': num_kana}
    return HttpResponse(json.dumps(data))


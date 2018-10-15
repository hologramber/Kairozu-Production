from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse
from main.models import Profile
from .models import Sandcastle, Resource
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


class ResourcesView(TemplateView):
    template_name = 'sandbox/resources.html'

    def get_context_data(self, **kwargs):
        context = super(ResourcesView, self).get_context_data(**kwargs)
        context['general'] = Resource.objects.filter(type__exact='general')
        context['edutility'] = Resource.objects.filter(type__exact='edutility')
        context['dictionary'] = Resource.objects.filter(type__exact='dictionary')
        context['kanji'] = Resource.objects.filter(type__exact='kanji')
        context['kana'] = Resource.objects.filter(type__exact='kana')
        context['edureading'] = Resource.objects.filter(type__exact='edureading')
        context['reference'] = Resource.objects.filter(type__exact='reference')
        context['video'] = Resource.objects.filter(type__exact='video')
        context['japan'] = Resource.objects.filter(type__exact='japan')
        context['exchange'] = Resource.objects.filter(type__exact='exchange')
        context['technical'] = Resource.objects.filter(type__exact='technical')
        context['other'] = Resource.objects.filter(type__exact='other')
        Profile.has_reviews(self.request.user)
        return context


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


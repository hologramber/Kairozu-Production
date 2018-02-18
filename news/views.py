from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post, FAQ, KnownIssue


def index(request):
    posts = Post.objects.filter(published=True)
    return render(request, 'news/index.html', {'posts': posts})


def post(request, slug):
    nowpost = get_object_or_404(Post, slug=slug)
    return render(request, 'news/post.html', {'post': nowpost})


class FAQView(ListView):
    template_name = 'news/faq.html'
    model = FAQ


class KnownIssuesView(ListView):
    template_name = 'news/knownissues.html'
    model = KnownIssue
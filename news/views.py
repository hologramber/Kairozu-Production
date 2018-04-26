from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Post, FAQ, KnownIssue, SiteIssue

def index(request):
    posts = Post.objects.filter(published=True)
    kaiposts = posts.filter(post_category__exact='KAI')
    nlpposts = posts.filter(post_category__exact='NLP')
    jpnposts = posts.filter(post_category__exact='JPN')
    return render(request, 'news/index.html', {'posts': posts, 'kaiposts': kaiposts, 'nlpposts': nlpposts, 'jpnposts': jpnposts})


def post(request, slug):
    nowpost = get_object_or_404(Post, slug=slug)
    return render(request, 'news/post.html', {'post': nowpost})


class FAQView(ListView):
    template_name = 'news/faq.html'
    model = FAQ


class KnownIssuesView(ListView):
    template_name = 'news/knownissues.html'
    model = KnownIssue


class AjaxTemplateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)


class NewIssueView(LoginRequiredMixin, AjaxTemplateMixin, CreateView):
    template_name = 'news/siteissue_form.html'
    model = SiteIssue
    fields = ['report_type', 'report_comment']

    def form_valid(self, form):
        if SiteIssue.objects.filter(report_by_user=self.request.user.id).count() >= 15:
            messages.add_message(self.request, messages.ERROR, 'Sorry! For the sake of my database, only 15 bug reports per day/user. Email kairozu@kairozu.com for help.')
        else:
            form.instance.report_by_user = self.request.user.id
            form.instance.report_from_url = self.request.META.get("HTTP_REFERER")
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Bug submitted! Apologies for the trouble, but thank you for letting me know!')
        if self.request.is_ajax():
            return render(self.request, 'news/siteissue_done.html')
        else:
            return render(self.request, 'index.html')
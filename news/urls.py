from django.conf.urls import url
from django.urls import path
from . import views
from news.feeds import RssSiteNewsFeed, AtomSiteNewsFeed

app_name = 'news'
urlpatterns = [
    url(r'^$', views.index, name='main'),
    path('rss/', RssSiteNewsFeed()),
    path('atom/', AtomSiteNewsFeed()),
    url(r'^faqlist/$', views.FAQView.as_view(), name='faq'),
    url(r'^knownissues/$', views.KnownIssuesView.as_view(), name='knownissues'),
    url(r'^newissue/$', views.NewIssueView.as_view(), name='issue'),
    url(r'^(?P<slug>[\w\-]+)/$', views.post, name='newspost'),
]
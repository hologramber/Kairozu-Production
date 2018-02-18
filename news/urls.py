from django.conf.urls import url
from . import views

app_name = 'news'
urlpatterns = [
    url(r'^$', views.index, name='main'),
    url(r'^faqlist/$', views.FAQView.as_view(), name='faq'),
    url(r'^knownissues/$', views.KnownIssuesView.as_view(), name='knownissues'),
    url(r'^(?P<slug>[\w\-]+)/$', views.post, name='newspost'),
]
from django.conf.urls import url
from . import views

app_name = 'sandbox'
urlpatterns = [
    url(r'^$', views.SandboxView.as_view(), name='main'),
    url(r'^japanesekana/$', views.japanesekana, name='japanesekana'),
    url(r'^joshi/$', views.joshi, name='joshi'),
    url(r'^kaimono/$', views.kaimono, name='kaimono'),
    url(r'^katakana/$', views.katakana, name='katakana'),
    url(r'^numbers/$', views.NumberQuizView.as_view(), name='numberquiz'),
    url(r'^numbers/grab/$', views.numquiz_grab, name='numbergrab'),
    url(r'^hiragana/$', views.hiragana, name='hiragana'),
    url(r'^resources/$', views.ResourcesView.as_view(), name='resources'),
]
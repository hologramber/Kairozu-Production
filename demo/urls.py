from django.conf.urls import url
from . import views, api_views

app_name = 'demo'
urlpatterns = [
    url(r'^$', views.demointerface, name='demointerface'),
    url(r'^intro/$', views.demointro, name='demointro'),
    url(r'^grammarlist/$', views.GrammarListView.as_view(), name='grammarlist'),
    url(r'^storydemo/$', views.storydemo, name='storydemo'),
    url(r'^dialoguedemo/$', views.dialoguedemo, name='dialoguedemo'),
    url(r'^demokana/$', views.demokana, name='demokana'),
    url(r'^vocablist/$', views.DemoVocabListView.as_view(), name='demovocablist'),
    url(r'^vocabquiz/$', views.DemoVocabQuizView.as_view(), name='demovocabquiz'),
    url(r'^vocabquiz/check/$', views.demo_vocab_check, name='demovocabcheck'),
    url(r'^vocabquiz/success/$', views.DemoVocabSuccessView.as_view(), name='demovocabsuccess'),
    url(r'^vocabquiz/grab/(?P<vindex>[0-9]+)/$', api_views.DemoVocabGrab.as_view(), name='demovocabgrab'),
    url(r'^expressionlist/$', views.DemoExpressionListView.as_view(), name='demoexpressionlist'),
    url(r'^expressionquiz/$', views.DemoExpressionQuizView.as_view(), name='demoexpressionquiz'),
    url(r'^expressionquiz/check/$', views.demo_expression_check, name='demoexpressioncheck'),
    url(r'^expressionquiz/success/$', views.DemoExpressionSuccessView.as_view(), name='demoexpressionsuccess'),
    url(r'^expressionquiz/grab/(?P<vindex>[0-9]+)/$', api_views.DemoExpressionGrab.as_view(), name='demoexpressiongrab'),
    url(r'^lesson/', views.demolesson, name='demolesson'),
    url(r'^practicequiz/$', views.DemoPracticeQuizView.as_view(), name='demopracticequiz'),
    url(r'^practicequiz/check/$', views.demo_practice_check, name='demopracticecheck'),
    url(r'^practicequiz/success/$', views.DemoPracticeSuccessView.as_view(), name='demopracticesuccess'),
    url(r'^practicequiz/grab/(?P<pindex>[0-9]+)/$', api_views.DemoPracticeGrab.as_view(), name='demopracticegrab'),
    url(r'^sentencequiz/$', views.DemoSentenceQuizView.as_view(), name='demosentencequiz'),
    url(r'^sentencequiz/check/$', views.demo_sentence_check, name='demosentencecheck'),
    url(r'^sentencequiz/success/$', views.DemoSentenceSuccessView.as_view(), name='demosentencesuccess'),
    url(r'^sentencequiz/grab/(?P<sindex>[0-9]+)/$', api_views.DemoSentenceGrab.as_view(), name='demosentencegrab'),
]

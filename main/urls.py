from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, api_views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='main'),                                                    # /main; main interface
    url(r'^chapter/(?P<chapter_id>[0-9]+)/$', views.ChapterInterfaceView.as_view(), name='interface'),    # /main/chapter/1; ch interface

    url(r'^chapter/(?P<chapter_id>[0-9]+)/vocablist/$', views.VocabListView.as_view(), name='vocablist'), # /main/chapter/1/vocablist
    url(r'^chapter/(?P<chapter_id>[0-9]+)/vocabquiz/$', views.VocabQuizView.as_view(), name='vocabquiz'), # /main/chapter/1/vocabquiz
    url(r'^chapter/(?P<chapter_id>[0-9]+)/vocabquiz/check/$', views.vocab_check, name='vocabcheck'),      # is vocab attempt correct?
    url(r'^chapter/(?P<chapter_id>[0-9]+)/vocabquiz/success/$', views.VocabSuccessView.as_view(), name='vocabsuccess'), # vocab quiz finished
    url(r'^chapter/(?P<chapter_id>[0-9]+)/vocabquiz/grab/$', api_views.VocabRecordGrab.as_view(), name='vocabgrab'), # grab next vocab for quiz

    url(r'^reviewvocab/$', views.ReviewVocabView.as_view(), name='reviewvocab'),
    url(r'^reviewvocab/check/$', views.reviewvocab_check, name='reviewvocabcheck'),
    url(r'^reviewvocab/current/$', views.ReviewVocabCurrentView.as_view(), name='reviewvocabcurrent'),
    url(r'^reviewvocab/grab/$', api_views.ReviewVocabRecordGrab.as_view(), name='reviewvocabgrab'),

    url(r'^chapter/(?P<chapter_id>[0-9]+)/expressionlist/$', views.ExpressionListView.as_view(), name='expressionlist'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/expressionquiz/$', views.ExpressionQuizView.as_view(), name='expressionquiz'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/expressionquiz/check/$', views.expression_check, name='expressioncheck'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/expressionquiz/success/$', views.ExpressionSuccessView.as_view(), name='expressionsuccess'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/expressionquiz/grab/$', api_views.ExpressionRecordGrab.as_view(), name='expressiongrab'),

    url(r'^reviewexpression/$', views.ReviewExpressionView.as_view(), name='reviewexpression'),
    url(r'^reviewexpression/check/$', views.reviewexpression_check, name='reviewexpressioncheck'),
    url(r'^reviewexpression/current/$', views.ReviewExpressionCurrentView.as_view(), name='reviewexpressioncurrent'),
    url(r'^reviewexpression/grab/$', api_views.ReviewExpressionRecordGrab.as_view(), name='reviewexpressiongrab'),

    url(r'^chapter/(?P<chapter_id>[0-9]+)/summary/$', views.SummaryView.as_view(), name='summary'),   # summary of chapter lessons

    url(r'^progress/$', views.ProgressView.as_view(), name='progress'),

    url(r'^lesson/(?P<lesson_id>[0-9]+)/$', views.LessonView.as_view(), name='lesson'),     # lesson interface
    url(r'^lesson/(?P<lesson_id>[0-9]+)/notes/$', views.GrammarNoteView.as_view(), name='grammarnote'),

    url(r'^lesson/(?P<lesson_id>[0-9]+)/practicequiz/$', views.PracticeQuizView.as_view(), name='practicequiz'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/practicequiz/check/$', views.practice_check, name='practicecheck'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/practicequiz/reset/$', views.practice_reset, name='practicereset'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/practicequiz/success/$', views.PracticeSuccessView.as_view(), name='practicesuccess'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/practicequiz/grab/(?P<pindex>[0-9]+)/$', api_views.PracticeGrab.as_view(), name='practicegrab'),

    url(r'^lesson/(?P<lesson_id>[0-9]+)/sentencequiz/$', views.SentenceQuizView.as_view(), name='sentencequiz'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/sentencequiz/check/$', views.sentence_check, name='sentencecheck'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/sentencequiz/success/$', views.SentenceSuccessView.as_view(), name='sentencesuccess'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/sentencequiz/grab/$', api_views.SentenceRecordGrab.as_view(), name='sentencegrab'),

    url(r'^reviewsentence/$', views.ReviewSentenceView.as_view(), name='reviewsentence'),
    url(r'^reviewsentence/check/$', views.reviewsentence_check, name='reviewsentencecheck'),
    url(r'^reviewsentence/current/$', views.ReviewSentenceCurrentView.as_view(), name='reviewsentencecurrent'),
    url(r'^reviewsentence/grab/$', api_views.ReviewSentenceRecordGrab.as_view(), name='reviewsentencegrab'),

    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercises/$', views.ExercisesView.as_view(), name='exercises'),

    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercise_p(?P<exercise_id>[0-9]+)/$', views.ExercisePassageView.as_view(), name='exercisepassage'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercise_p(?P<exercise_id>[0-9]+)/check/$', views.exercise_passage_check, name='exercisepassagecheck'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercise_p(?P<exercise_id>[0-9]+)/grade/$', views.exercise_passage_grade, name='exercisepassagegrade'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercise_p(?P<exercise_id>[0-9]+)/grab/(?P<passage_index>[0-9]+)$', api_views.ExercisePassageGrab.as_view(), name='exercisepassagegrab'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercise_p(?P<exercise_id>[0-9]+)/success/$', views.ExercisePassageSuccessView.as_view(), name='exercisepassagesuccess'),

    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercise_d(?P<exercise_id>[0-9]+)/$', views.ExerciseDialogueView.as_view(), name='exercisedialogue'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercise_d(?P<exercise_id>[0-9]+)/check/$', views.exercise_dialogue_check, name='exercisedialoguecheck'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercise_d(?P<exercise_id>[0-9]+)/grade/$', views.exercise_dialogue_grade, name='exercisedialoguegrade'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercise_d(?P<exercise_id>[0-9]+)/grab/(?P<dialogue_index>[0-9]+)$', api_views.ExerciseDialogueGrab.as_view(), name='exercisedialoguegrab'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/exercise_d(?P<exercise_id>[0-9]+)/success/$', views.ExerciseDialogueSuccessView.as_view(), name='exercisedialoguesuccess'),

    # url(r'^api/vocablist/$', api_views.VocabularyList.as_view()),   # (api) /main/api/vocablist; vocabulary API view
    # url(r'^api/vocabdetail/(?P<pk>[0-9]+)/$', api_views.VocabularyDetail.as_view()),   # (api) vocabulary API detail view
    # url(r'^api/vocabrecordlist/$', api_views.VocabRecordList.as_view()),   # (api) /main/api/vocabrecordlist; vocabrecord API view
    # url(r'^api/vocabrecorddetail/(?P<pk>[0-9]+)/$', api_views.VocabRecordDetail.as_view()),    # (api) vocabrecord API detail view
    #
    # url(r'^api/sentencelist/$', api_views.SentenceList.as_view()), # (api) /main/api/sentencelist; sentence API view
    # url(r'^api/sentencedetail/(?P<pk>[0-9]+)/$', api_views.SentenceDetail.as_view()),  # (api) sentence API detail view
    # url(r'^api/sentencerecordlist/$', api_views.SentenceRecordList.as_view()),
    # url(r'^api/sentencerecorddetail/(?P<pk>[0-9]+)/$', api_views.SentenceRecordDetail.as_view()),
    #
    # url(r'^api/practicelist/$', api_views.PracticeList.as_view()),  # (api) /main/api/practicelist; practice API view
    # url(r'^api/practicedetail/(?P<pk>[0-9]+)/$', api_views.PracticeDetail.as_view()),   # (api) practice API detail view

    # url(r'^api/profile/(?P<pk>[0-9]+)/$', api_views.ProfileDetail.as_view()),
    # url(r'^exercises/(?P<chapter_id>[0-9]+)/$', views.ExercisesAdminView.as_view()),
    # url(r'^adm/sentences/(?P<fix_id>[0-9]+)/$', api_views.SentenceAdminFixView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

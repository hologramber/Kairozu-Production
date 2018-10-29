from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, api_views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='main'),                                                    # /main; main interface
    url(r'^chapter/(?P<chapter_id>[0-9]+)/$', views.ChapterInterfaceView.as_view(), name='interface'),    # /main/chapter/1; ch interface
    url(r'^lesson/(?P<lesson_id>[0-9]+)/$', views.LessonView.as_view(), name='lesson'),                   # lesson interface
    url(r'^lesson/(?P<lesson_id>[0-9]+)/notes/$', views.GrammarNoteView.as_view(), name='grammarnote'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/summary/$', views.SummaryView.as_view(), name='summary'),       # summary of ch lessons

    url(r'^flashcards/$', views.FlashcardSetListView.as_view(), name='flashcardsetlist'),
    url(r'^flashcards/create/$', views.FlashcardSetCreateView.as_view(), name='flashcardsetcreate'),
    url(r'^flashcards/all/$', views.FlashcardListViewAll.as_view(), name='flashcardlist'),
    url(r'^flashcards/batch/$', views.flashcard_batch_csv, name='flashcardbatch'),
    url(r'^flashcards/(?P<slug>[\w\-]+)/$', views.FlashcardSetDetailView.as_view(), name='flashcardsetdetail'),
    url(r'^flashcards/(?P<slug>[\w\-]+)/update/$', views.FlashcardSetUpdateView.as_view(), name='flashcardsetupdate'),
    url(r'^flashcards/(?P<slug>[\w\-]+)/delete/$', views.FlashcardSetDeleteView.as_view(), name='flashcardsetdelete'),

    url(r'^flashcards/(?P<slug>[\w\-]+)/create/$', views.FlashcardCreateView.as_view(), name='flashcardcreate'),
    url(r'^flashcards/(?P<slug>[\w\-]+)/(?P<card_id>[0-9]+)/$', views.FlashcardUpdateView.as_view(), name='flashcardupdate'),
    url(r'^flashcards/(?P<slug>[\w\-]+)/(?P<card_id>[0-9]+)/delete/$', views.FlashcardDeleteView.as_view(), name='flashcarddelete'),

    # ################## VOCABULARY ####################
    url(r'^chapter/(?P<chapter_id>[0-9]+)/vocablist/$', views.VocabListView.as_view(), name='vocablist'), # /main/chapter/1/vocablist
    url(r'^chapter/(?P<chapter_id>[0-9]+)/vocabquiz/$', views.VocabQuizView.as_view(), name='vocabquiz'), # /main/chapter/1/vocabquiz
    url(r'^chapter/(?P<chapter_id>[0-9]+)/vocabquiz/finish/$', views.vocabfinish, name='vocabfinish'),
    url(r'^chapter/(?P<chapter_id>[0-9]+)/vocabquiz/success/$', views.VocabSuccessView.as_view(), name='vocabsuccess'), # vocab quiz finished
    url(r'^chapter/(?P<chapter_id>[0-9]+)/vocabquiz/grab/$', api_views.VocabGrab.as_view(), name='vocabgrab'), # grab next vocab for quiz

    # ################## PRACTICES #####################
    url(r'^lesson/(?P<lesson_id>[0-9]+)/practicequiz/$', views.PracticeQuizView.as_view(), name='practicequiz'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/practicequiz/grab/$', api_views.PracticeGrab.as_view(), name='practicegrab'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/practicequiz/finish/$', views.practicefinish, name='practicefinish'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/practicequiz/success/$', views.PracticeSuccessView.as_view(), name='practicesuccess'),

    # ################## SENTENCES #####################
    url(r'^lesson/(?P<lesson_id>[0-9]+)/sentencequiz/$', views.SentenceQuizView.as_view(), name='sentencequiz'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/sentencequiz/finish/$', views.sentencefinish, name='sentencefinish'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/sentencequiz/success/$', views.SentenceSuccessView.as_view(), name='sentencesuccess'),
    url(r'^lesson/(?P<lesson_id>[0-9]+)/sentencequiz/grab/$', api_views.SentenceGrab.as_view(), name='sentencegrab'),

    # ################## REVIEWS #######################
    url(r'^reviewflashcard/$', views.ReviewFlashcardView.as_view(), name='reviewflashcard'),
    url(r'^reviewflashcard/quick/$', views.ReviewFlashcardQuickView.as_view(), name='reviewflashcardquick'),
    url(r'^reviewflashcard/save/$', views.reviewflashcardsave, name='reviewflashcardsave'),
    url(r'^reviewflashcard/current/$', views.ReviewFlashcardCurrentView.as_view(), name='reviewflashcardcurrent'),
    url(r'^reviewflashcard/grab/(?P<set_slug>[\w\-]+)/$', api_views.ReviewFlashcardGrab.as_view()),
    url(r'^reviewflashcard/grab/$', api_views.ReviewFlashcardGrab.as_view(), name='reviewflashcardgrab'),
    url(r'^reviewflashcard/(?P<set_slug>[\w\-]+)/quick/$', views.ReviewFlashcardQuickView.as_view(), name='reviewflashcardquick'),
    url(r'^reviewflashcard/(?P<set_slug>[\w\-]+)/$', views.ReviewFlashcardView.as_view(), name='reviewflashcard'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

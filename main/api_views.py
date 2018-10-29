from datetime import datetime
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Vocabulary, Practice, Sentence, Flashcard
from . import serializers


class VocabGrab(generics.ListAPIView):
    serializer_class = serializers.VocabularySerializer

    def get_queryset(self):
        chapter_id = int(self.kwargs['chapter_id'])
        vocabwords = Vocabulary.objects.filter(chapter_id__exact=chapter_id)
        return vocabwords


class PracticeGrab(generics.ListAPIView):
    serializer_class = serializers.PracticeSerializer

    def get_queryset(self):
        lesson_id = int(self.kwargs['lesson_id'])
        practices = Practice.objects.filter(lesson_id__exact=lesson_id)
        return practices


class SentenceGrab(generics.ListAPIView):
    serializer_class = serializers.SentenceSerializer

    def get_queryset(self):
        lesson_id = int(self.kwargs['lesson_id'])
        srecords = Sentence.objects.filter(lesson__id__exact=lesson_id)
        return srecords


class ReviewFlashcardGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.FlashcardSerializer

    def get_queryset(self):
        if 'set_slug' in self.kwargs:
            frecords = Flashcard.objects.filter(user_id=self.request.user.id, set__slug__exact=self.kwargs['set_slug'], next_review__lte=datetime.now())[:50]
        else:
            frecords = Flashcard.objects.filter(user_id=self.request.user.id, next_review__lte=datetime.now())[:50]
        if not frecords:
            frecords = Flashcard.objects.none()
        return frecords
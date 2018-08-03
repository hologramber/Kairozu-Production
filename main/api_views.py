from datetime import datetime
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Practice, VocabRecord, Profile, SentenceRecord, ExpressionRecord, ExercisePrompt, ExerciseSentence, Flashcard
from . import serializers


class VocabRecordGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.VocabRecordSerializer

    def get_queryset(self):
        chapter_id = int(self.kwargs['chapter_id'])
        if chapter_id < self.request.user.profile.currentvocab:
            vrecords = VocabRecord.objects.filter(user_id=self.request.user.id, vocab__chapter__id__exact=chapter_id).order_by('last_attempt')
        elif chapter_id == self.request.user.profile.currentvocab:
            vrecords = VocabRecord.objects.filter(user_id=self.request.user.id, vocab__chapter__id__exact=chapter_id, rating__lte=0).order_by('last_attempt')
            if vrecords is None:
                Profile.graduate_vocab(self.request.user, chapter_id)
                vrecords = VocabRecord.objects.none()
        else:
            vrecords = VocabRecord.objects.none()
        return vrecords


class ReviewVocabRecordGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.VocabRecordSerializer

    def get_queryset(self):
        vrecords = VocabRecord.objects.filter(user_id=self.request.user.id, next_review__lte=datetime.now())[:50]
        if vrecords is None:
            vrecords = VocabRecord.objects.none()
        return vrecords


class ExpressionRecordGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.ExpressionRecordSerializer

    def get_queryset(self):
        chapter_id = int(self.kwargs['chapter_id'])
        if chapter_id < self.request.user.profile.currentexpression:
            erecords = ExpressionRecord.objects.filter(user_id=self.request.user.id, express__chapter__id__exact=chapter_id).order_by('last_attempt')
        elif chapter_id == self.request.user.profile.currentexpression:
            erecords = ExpressionRecord.objects.filter(user_id=self.request.user.id, express__chapter__id__exact=chapter_id, rating__lte=0).order_by('last_attempt')
            if erecords is None:
                Profile.graduate_expression(self.request.user, chapter_id)
                erecords = ExpressionRecord.objects.none()
        else:
            erecords = ExpressionRecord.objects.none()
        return erecords


class ReviewExpressionRecordGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.ExpressionRecordSerializer

    def get_queryset(self):
        erecords = ExpressionRecord.objects.filter(user_id=self.request.user.id, next_review__lte=datetime.now())[:50]
        if erecords is None:
            erecords = ExpressionRecord.objects.none()
        return erecords


class PracticeGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.PracticeSerializer

    def get_queryset(self):
        lesson_id = int(self.kwargs['lesson_id'])
        if lesson_id <= self.request.user.profile.currentpractice:
            practices = Practice.objects.filter(lesson_id__exact=lesson_id)
        else:
            practices = Practice.objects.none()
        return practices


class SentenceRecordGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.SentenceRecordSerializer

    def get_queryset(self):
        lesson_id = int(self.kwargs['lesson_id'])
        if lesson_id < self.request.user.profile.currentlesson:
            srecords = SentenceRecord.objects.filter(user_id=self.request.user.id, sentence__lesson__id__exact=lesson_id).order_by('last_attempt')
        elif lesson_id == self.request.user.profile.currentlesson:
            srecords = SentenceRecord.objects.filter(user_id=self.request.user.id, sentence__lesson__id__exact=lesson_id, rating__lte=0).order_by('last_attempt')
            if srecords is None:
                Profile.graduate_lesson(self.request.user, lesson_id)
                srecords = SentenceRecord.objects.none()
        else:
            srecords = SentenceRecord.objects.none()
        return srecords


class ReviewSentenceRecordGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.SentenceRecordSerializer

    def get_queryset(self):
        srecords = SentenceRecord.objects.filter(user_id=self.request.user.id, next_review__lte=datetime.now())[:50]
        if srecords is None:
            srecords = SentenceRecord.objects.none()
        return srecords


class PassageGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.ExerciseSentenceSerializer

    def get_queryset(self):
        exercise_id = int(self.kwargs['exercise_id'])
        if exercise_id <= self.request.user.profile.currentexercise:
            exercise_sentences = ExerciseSentence.objects.filter(exercise_id=exercise_id)
        else:
            exercise_sentences = ExerciseSentence.objects.none()
        return exercise_sentences


class DialogueGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.ExercisePromptSerializer

    def get_queryset(self):
        exercise_id = int(self.kwargs['exercise_id'])
        if exercise_id <= self.request.user.profile.currentexercise:
            exercise_prompts = ExercisePrompt.objects.filter(exercise_id=exercise_id)
        else:
            exercise_prompts = ExercisePrompt.objects.none()
        return exercise_prompts


class ReviewFlashcardGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.FlashcardSerializer

    def get_queryset(self):
        frecords = Flashcard.objects.filter(user_id=self.request.user.id, next_review__lte=datetime.now())[:50]
        if frecords is None:
            frecords = Flashcard.objects.none()
        return frecords
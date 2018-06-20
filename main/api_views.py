from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Practice, VocabRecord, Profile, SentenceRecord, ExpressionRecord, ExercisePrompt, ExerciseSentence
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
        else:
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
        else:
            erecords = ExpressionRecord.objects.none()
        return erecords


class ReviewExpressionRecordGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.ExpressionRecordSerializer

    def get_object(self):
        now = datetime.now()
        next_expression = ExpressionRecord.objects.filter(user_id=self.request.user.id, next_review__lte=now).first()
        return next_expression


class ReviewVocabRecordGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.VocabRecordSerializer

    def get_object(self):
        now = datetime.now()
        next_vocab = VocabRecord.objects.filter(user_id=self.request.user.id, next_review__lte=now).first()
        return next_vocab


class PracticeGrab(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.PracticeSerializer

    def get_queryset(self):
        lesson_id = int(self.kwargs['lesson_id'])
        if lesson_id <= self.request.user.profile.currentpractice:
            practices = Practice.objects.filter(lesson_id__exact=lesson_id)
        else:
            practices = Practice.objects.none()
        return practices


class SentenceRecordGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.SentenceRecordSerializer

    def get_object(self):
        lesson_id = int(self.kwargs['lesson_id'])

        if self.request.user.profile.currentlesson > lesson_id:
            next_sentence = SentenceRecord.objects.filter(user_id=self.request.user.id, sentence__lesson__id__exact=lesson_id).order_by('last_attempt').first()
        else:
            next_sentence = SentenceRecord.objects.filter(user_id=self.request.user.id, sentence__lesson__id__exact=lesson_id, rating__lte=0).order_by('last_attempt').first()
            if next_sentence is None and self.request.user.profile.currentlesson == lesson_id:
                Profile.graduate_lesson(self.request.user, lesson_id)
        return next_sentence


class ReviewSentenceRecordGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.SentenceRecordSerializer

    def get_object(self):
        now = datetime.now()
        next_sentence = SentenceRecord.objects.filter(user_id=self.request.user.id, next_review__lte=now).first()
        return next_sentence


class ExercisePassageGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.ExerciseSentenceSerializer

    def get_object(self):
        exercise_id = int(self.kwargs['exercise_id'])
        passage_index = int(self.kwargs['passage_index'])
        next_sentence = ExerciseSentence.objects.filter(exercise_id=exercise_id)

        if len(next_sentence) > passage_index:
            next_sentence = next_sentence[passage_index]
            return next_sentence
        else:
            return None


class ExerciseDialogueGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.ExercisePromptSerializer

    def get_object(self):
        exercise_id = int(self.kwargs['exercise_id'])
        dialogue_index = int(self.kwargs['dialogue_index'])
        next_prompt = ExercisePrompt.objects.filter(exercise_id=exercise_id)

        if len(next_prompt) > dialogue_index:
            next_prompt = next_prompt[dialogue_index]
            return next_prompt
        else:
            return None

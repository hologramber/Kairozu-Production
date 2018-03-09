from datetime import datetime
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Practice, VocabRecord, Profile, SentenceRecord, ExpressionRecord, ExercisePrompt, ExerciseSentence
from . import serializers

class VocabRecordGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.VocabRecordSerializer

    def get_object(self):
        chapter_id = int(self.kwargs['chapter_id'])
        if self.request.user.profile.currentvocab > chapter_id:
            next_vocab = VocabRecord.objects.filter(user_id=self.request.user.id, vocab__chapter__id__exact=chapter_id).order_by('last_attempt').first()
        else:
            next_vocab = VocabRecord.objects.filter(user_id=self.request.user.id, vocab__chapter__id__exact=chapter_id, rating__lte=0).order_by('last_attempt').first()
            if next_vocab is None and self.request.user.profile.currentvocab == chapter_id:
                Profile.graduate_vocab(self.request.user, chapter_id)
        return next_vocab


class ExpressionRecordGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.ExpressionRecordSerializer

    def get_object(self):
        chapter_id = int(self.kwargs['chapter_id'])
        if self.request.user.profile.currentexpression > chapter_id:
            next_expression = ExpressionRecord.objects.filter(user_id=self.request.user.id, express__chapter__id__exact=chapter_id).order_by('last_attempt').first()
        else:
            next_expression = ExpressionRecord.objects.filter(user_id=self.request.user.id, express__chapter__id__exact=chapter_id, rating__lte=0).order_by('last_attempt').first()
            if next_expression is None and self.request.user.profile.currentexpression == chapter_id:
                Profile.graduate_expression(self.request.user, chapter_id)
        return next_expression


class ReviewExpressionRecordGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.ExpressionRecordSerializer

    def get_object(self):
        now = datetime.now()
        next_expression = ExpressionRecord.objects.filter(user_id=self.request.user.id, next_review__lte=now).order_by('last_attempt').first()
        return next_expression


class ReviewVocabRecordGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.VocabRecordSerializer

    def get_object(self):
        now = datetime.now()
        next_vocab = VocabRecord.objects.filter(user_id=self.request.user.id, next_review__lte=now).order_by('last_attempt').first()
        return next_vocab


class PracticeGrab(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = serializers.PracticeSerializer

    def get_object(self):
        lesson_id = int(self.kwargs['lesson_id'])
        pindex = int(self.kwargs['pindex'])
        next_practice = Practice.objects.filter(lesson_id=lesson_id)

        if len(next_practice) > pindex:
            next_practice = next_practice[pindex]
            return next_practice
        else:
            if self.request.user.profile.currentpractice == lesson_id:
                Profile.graduate_practice(self.request.user, lesson_id)
            return None


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
        next_sentence = SentenceRecord.objects.filter(user_id=self.request.user.id, next_review__lte=now).order_by('last_attempt').first()
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

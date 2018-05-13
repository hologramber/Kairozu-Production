from rest_framework import serializers
from .models import Sentence, Practice, Vocabulary, VocabRecord, SentenceRecord, Expression, ExpressionRecord, ExerciseResponse, ExercisePrompt, ExerciseSentence


class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        exclude = ('partofspeech','kana','kanji',)


class VocabRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    vocab = VocabularySerializer()

    class Meta:
        model = VocabRecord
        fields = '__all__'


class ExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expression
        exclude = ('kana','kanji',)


class ExpressionRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    express = ExpressionSerializer()

    class Meta:
        model = ExpressionRecord
        fields = '__all__'


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        exclude = ('kana','kanji',)


class SentenceRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    sentence = SentenceSerializer()

    class Meta:
        model = SentenceRecord
        fields = '__all__'


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        exclude = ('pone_kana','ptwo_kana','pone_kanji','ptwo_kanji','vieworder',)


class ExerciseResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseResponse
        exclude = ('response_order','response_kana','response_kanji',)


class ExercisePromptSerializer(serializers.ModelSerializer):
    responses = ExerciseResponseSerializer(many=True, read_only=True)

    class Meta:
        model = ExercisePrompt
        fields = '__all__'


class ExerciseSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSentence
        exclude = ('kana','kanji','display_order',)

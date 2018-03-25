from rest_framework import serializers
from .models import Sentence, Practice, Vocabulary, VocabRecord, SentenceRecord, Expression, ExpressionRecord, ExerciseResponse, ExercisePrompt, ExerciseSentence


class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        exclude = ('partofspeech',)


class VocabRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    vocab = VocabularySerializer()

    class Meta:
        model = VocabRecord
        fields = '__all__'


class ExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expression
        fields = '__all__'


class ExpressionRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    express = ExpressionSerializer()

    class Meta:
        model = ExpressionRecord
        fields = '__all__'


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = '__all__'


class SentenceRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    sentence = SentenceSerializer()

    class Meta:
        model = SentenceRecord
        fields = '__all__'


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        fields = '__all__'


class ExerciseResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseResponse
        fields = '__all__'


class ExercisePromptSerializer(serializers.ModelSerializer):
    responses = ExerciseResponseSerializer(many=True, read_only=True)

    class Meta:
        model = ExercisePrompt
        fields = '__all__'


class ExerciseSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSentence
        fields = '__all__'

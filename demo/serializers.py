from rest_framework import serializers
from .models import DemoSentence, DemoPractice, DemoVocab, DemoExpression


class DemoVocabSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoVocab
        fields = '__all__'


class DemoExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoExpression
        fields = '__all__'


class DemoSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoSentence
        fields = '__all__'


class DemoPracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoPractice
        fields = '__all__'


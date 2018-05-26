from rest_framework import generics
from .models import DemoVocab, DemoSentence, DemoPractice, DemoExpression
from . import serializers


class DemoVocabGrab(generics.ListAPIView):
    serializer_class = serializers.DemoVocabSerializer
    queryset = DemoVocab.objects.all()


class DemoExpressionGrab(generics.ListAPIView):
    serializer_class = serializers.DemoExpressionSerializer
    queryset = DemoExpression.objects.all()


class DemoPracticeGrab(generics.ListAPIView):
    serializer_class = serializers.DemoPracticeSerializer
    queryset = DemoPractice.objects.all()


class DemoSentenceGrab(generics.ListAPIView):
    serializer_class = serializers.DemoSentenceSerializer
    queryset = DemoSentence.objects.all()

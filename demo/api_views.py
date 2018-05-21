from rest_framework import generics
from .models import DemoVocab, DemoSentence, DemoPractice, DemoExpression
from . import serializers


class DemoVocabGrab(generics.RetrieveAPIView):
    serializer_class = serializers.DemoVocabSerializer

    def get_object(self):
        vindex = int(self.kwargs['vindex'])
        next_vocab = DemoVocab.objects.all()

        if len(next_vocab) > vindex:
            next_vocab = next_vocab[vindex]
        else:
            next_vocab = DemoVocab.objects.filter(id__lt=0).first()
        return next_vocab


class DemoExpressionGrab(generics.RetrieveAPIView):
    serializer_class = serializers.DemoExpressionSerializer

    def get_object(self):
        vindex = int(self.kwargs['eindex'])
        next_expression = DemoExpression.objects.all()

        if len(next_expression) > vindex:
            next_expression = next_expression[vindex]
        else:
            next_expression = DemoExpression.objects.filter(id__lt=0).first()
        return next_expression


class DemoPracticeGrab(generics.RetrieveAPIView):
    serializer_class = serializers.DemoPracticeSerializer

    def get_object(self):
        pindex = int(self.kwargs['pindex'])
        next_practice = DemoPractice.objects.all()

        if len(next_practice) > pindex:
            next_practice = next_practice[pindex]
        else:
            next_practice = DemoPractice.objects.filter(id__lt=0).first()
        return next_practice


class DemoSentenceGrab(generics.RetrieveAPIView):
    serializer_class = serializers.DemoSentenceSerializer

    def get_object(self):
        sindex = int(self.kwargs['sindex'])
        next_sentence = DemoSentence.objects.all()

        if len(next_sentence) > sindex:
            next_sentence = next_sentence[sindex]
        else:
            next_sentence = DemoSentence.objects.filter(id__lt=0).first()
        return next_sentence

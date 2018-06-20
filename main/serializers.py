from rest_framework import serializers
from .models import Sentence, Practice, Vocabulary, VocabRecord, SentenceRecord, Expression, ExpressionRecord, ExerciseResponse, ExercisePrompt, ExerciseSentence


class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        exclude = ('partofspeech','kana','kanji',)


class RecordListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        record_mapping = {record.id: record for record in instance}     # id -> instance
        data_mapping = {item['id']: item for item in validated_data}    # id -> data item

        record_multi = []
        for record_id, data in data_mapping.items():
            record = record_mapping.get(record_id, None)
            if record is not None:
                record_multi.append(self.child.update(record, data))

        # # deletions
        # for record_id, record in record_mapping.items():
        #     if record_id not in data_mapping:
        #         print(record)

        return record_multi

class VocabRecordSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user = serializers.StringRelatedField()
    vocab = VocabularySerializer(read_only=True)

    class Meta:
        model = VocabRecord
        fields = '__all__'
        list_serializer_class = RecordListSerializer


class ExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expression
        exclude = ('kana','kanji',)


class ExpressionRecordSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user = serializers.StringRelatedField()
    express = ExpressionSerializer(read_only=True)

    class Meta:
        model = ExpressionRecord
        fields = '__all__'
        list_serializer_class = RecordListSerializer


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        exclude = ('kana','kanji',)


class SentenceRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    sentence = SentenceSerializer(read_only=True)

    class Meta:
        model = SentenceRecord
        fields = '__all__'


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        exclude = ('pone_kana','ptwo_kana','pone_kanji','ptwo_kanji',)


class ExerciseResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseResponse
        exclude = ('response_order','response_kana','response_kanji',)


class ExercisePromptSerializer(serializers.ModelSerializer):
    responses = ExerciseResponseSerializer(many=True, read_only=True)

    class Meta:
        model = ExercisePrompt
        exclude = ('prompt_kana',)


class ExerciseSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSentence
        exclude = ('kana','kanji','display_order',)

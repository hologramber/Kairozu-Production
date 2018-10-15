from rest_framework import serializers
from .models import Sentence, Practice, Vocabulary, Flashcard


class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        exclude = ('partofspeech','kana','kanji',)


class RecordListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # record_mapping = vocab records, creates a dictionary of { vocabrecord.id: vocabrecord }
        record_mapping = {record.id: record for record in instance}     # id -> instance
        # data_mapping = creates a dictionary of { vocabrecord.id: validated-vocabrecord-data }
        data_mapping = {item['id']: item for item in validated_data}    # id -> data item

        record_multi = []
        for record_id, data in data_mapping.items():
            record = record_mapping.get(record_id, None)
            if record is not None:
                record_multi.append(self.child.update(record, data))

        # # if you want to delete records not in data_mapping
        # for record_id, record in record_mapping.items():
        #     if record_id not in data_mapping:
        #         print(record)

        return record_multi


class FlashcardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user = serializers.StringRelatedField()
    class Meta:
        model = Flashcard
        exclude = ('kana', 'kanji',)
        list_serializer_class = RecordListSerializer


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        exclude = ('kana','kanji',)


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        exclude = ('pone_kana','ptwo_kana','pone_kanji','ptwo_kanji',)
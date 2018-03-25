from datetime import datetime

from main.models import Profile
from main.models import Vocabulary
from main.models import Expression
from main.models import Sentence
from main.models import VocabRecord
from main.models import ExpressionRecord
from main.models import SentenceRecord

profiles = Profile.objects.all()

for prof in profiles:
    # uservocab = prof.currentvocab
    # userexpression = prof.currentexpression
    # usersentence = prof.currentlesson

    vocabrecords = VocabRecord.objects.filter(user_id=prof.user.id)
    for vr in vocabrecords:
        if vr.last_attempt is None:
                vr.last_attempt = datetime.now()
                vr.save()

    expressionrecords = ExpressionRecord.objects.filter(user_id=prof.user.id)
    for er in expressionrecords:
        if er.last_attempt is None:
            er.last_attempt = datetime.now()
            er.save()

    sentencerecords = SentenceRecord.objects.filter(user_id=prof.user.id)
    for sr in sentencerecords:
        if sr.last_attempt is None:
            sr.last_attempt = datetime.now()
            sr.save()

    # vocabulary = Vocabulary.objects.filter(chapter_id__lte=uservocab)
    # if len(vocabulary) == 0:
    #     pass
    # else:
    #     for vocab in vocabulary:
    #         VocabRecord.objects.get_or_create(user=prof.user, vocab=vocab, last_attempt=datetime.now())
    #
    # vocabrecords = VocabRecord.objects.filter(user_id=prof.user.id)
    # for vr in vocabrecords:
    #     if vr.vocab.chapter_id < uservocab and vr.next_review is None:
    #             vr.next_review = datetime.now()
    #             vr.last_attempt = datetime.now()
    #             vr.rating = 1
    #             vr.save()
    #
    # expressions = Expression.objects.filter(chapter_id__lte=userexpression)
    # if len(expressions) == 0:
    #     pass
    # else:
    #     for express in expressions:
    #         ExpressionRecord.objects.get_or_create(user=prof.user, express=express, last_attempt=datetime.now())
    #
    # expressionrecords = ExpressionRecord.objects.filter(user_id=prof.user.id)
    # for er in expressionrecords:
    #     if er.express.chapter_id < userexpression and er.next_review is None:
    #         er.next_review = datetime.now()
    #         er.last_attempt = datetime.now()
    #         er.rating = 1
    #         er.save()
    #
    # sentences = Sentence.objects.filter(lesson_id__lte=usersentence)
    # if len(sentences) == 0:
    #     pass
    # else:
    #     for sent in sentences:
    #         SentenceRecord.objects.get_or_create(user=prof.user, sentence=sent, last_attempt=datetime.now())
    #
    # sentencerecords = SentenceRecord.objects.filter(user_id=prof.user.id)
    # for sr in sentencerecords:
    #     if sr.sentence.lesson_id < usersentence and sr.next_review is None:
    #         sr.next_review = datetime.now()
    #         sr.last_attempt = datetime.now()
    #         sr.rating = 1
    #         sr.save()
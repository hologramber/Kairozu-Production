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

    keep_vr = []
    vocabrecords = VocabRecord.objects.filter(user_id=prof.user.id).order_by('vocab__id', 'id')
    for vr in vocabrecords:
        if vr.vocab.id in keep_vr:
            vr.delete()
        else:
            keep_vr.append(vr.vocab.id)

    keep_sr = []
    sentencerecords = SentenceRecord.objects.filter(user_id=prof.user.id).order_by('sentence__id', 'id')
    for sr in sentencerecords:
        if sr.sentence.id in keep_sr:
            sr.delete()
        else:
            keep_sr.append(sr.sentence.id)

    keep_er = []
    expressionrecords = ExpressionRecord.objects.filter(user_id=prof.user.id).order_by('express__id', 'id')
    for er in expressionrecords:
        if er.express.id in keep_er:
            er.delete()
        else:
            keep_er.append(er.express.id)



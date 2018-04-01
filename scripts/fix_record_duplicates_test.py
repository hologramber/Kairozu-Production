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

    keeprecords = []
    vocabrecords = VocabRecord.objects.filter(user_id=prof.user.id).order_by('vocab__id', 'id')
    for vr in vocabrecords:
        if vr.id in keeprecords:
            vr.rating = 333
            vr.save()
        else:
            keeprecords.append(vr.id)



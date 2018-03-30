from main.models import Sentence
from main.models import Practice

practices13 = Practice.objects.filter(lesson_id__exact=13)
practices14 = Practice.objects.filter(lesson_id__exact=14)
practices15 = Practice.objects.filter(lesson_id__exact=15)
practices16 = Practice.objects.filter(lesson_id__exact=16)

sentences13 = Sentence.objects.filter(lesson_id__exact=13)
sentences14 = Sentence.objects.filter(lesson_id__exact=14)
sentences15 = Sentence.objects.filter(lesson_id__exact=15)
sentences16 = Sentence.objects.filter(lesson_id__exact=16)

for sentence in sentences13:
    sentence.lesson_id = 56
    sentence.save()

for practice in practices13:
    practice.lesson_id = 56
    sentence.save()

for sentence in sentences16:
    sentence.lesson_id = 13
    sentence.save()

for practice in practices16:
    practice.lesson_id = 13
    sentence.save()

for sentence in sentences15:
    sentence.lesson_id = 16
    sentence.save()

for practice in practices15:
    practice.lesson_id = 16
    sentence.save()

for sentence in sentences14:
    sentence.lesson_id = 15
    sentence.save()

for practice in practices14:
    practice.lesson_id = 15
    sentence.save()

for sentence in sentences13:
    sentence.lesson_id = 14
    sentence.save()

for practice in practices13:
    practice.lesson_id = 14
    sentence.save()
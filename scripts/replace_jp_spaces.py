# import re
# from main.models import Vocabulary
# from main.models import Expression
from main.models import Sentence
from main.models import Practice
# from main.models import Lesson
# from main.models import ExercisePrompt
# from main.models import ExerciseSentence
# from main.models import ExerciseResponse
# from main.models import Example

# words = Vocabulary.objects.all()
# express = Expression.objects.all()
sentences = Sentence.objects.all()
practices = Practice.objects.all()
# lessons = Lesson.objects.all()
# prompts = ExercisePrompt.objects.all()
# exsents = ExerciseSentence.objects.all()
# exresps = ExerciseResponse.objects.all()
# examples = Example.objects.all()

# for word in words:
    # expression.kana = re.sub('。', '｡', expression.kana)
    # expression.kana = re.sub('、[ 　]*', '､ ', expression.kana)
    # expression.kana = re.sub(r'[ 　]+', ' ', expression.kana)
    # expression.kanji = re.sub('。', '｡', expression.kanji)
    # expression.kanji = re.sub('、[ 　]*', '､ ', expression.kanji)
    # expression.kanji = re.sub(r'[ 　]+', ' ', expression.kanji)
    # word.save()

# for expression in express:
#     expression.save()

for sentence in sentences:
    sentence.save()

for practice in practices:
    practice.save()

# for lesson in lessons:
#     lesson.save()

# for prompt in prompts:
#     prompt.save()
#
# for exsent in exsents:
#     exsent.save()
#
# for exresp in exresps:
#     exresp.save()
#
# for example in examples:
#     example.save()
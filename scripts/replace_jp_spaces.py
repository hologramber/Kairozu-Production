import re
from main.models import Expression

expressions = Expression.objects.all()

for expression in expressions:
    # expression.kana = re.sub('。', '｡', expression.kana)
    # expression.kana = re.sub('、[ 　]*', '､ ', expression.kana)
    # expression.kana = re.sub(r'[ 　]+', ' ', expression.kana)
    #
    # expression.kanji = re.sub('。', '｡', expression.kanji)
    # expression.kanji = re.sub('、[ 　]*', '､ ', expression.kanji)
    # expression.kanji = re.sub(r'[ 　]+', ' ', expression.kanji)

    expression.save()
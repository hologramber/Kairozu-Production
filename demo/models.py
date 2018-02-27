import re
from django.db import models


class BetaEmail(models.Model):
    user_beta_email = models.EmailField(max_length=50, unique=True)
    user_beta_submitted = models.DateTimeField(auto_now_add=True, blank=True)


class DemoSentence(models.Model):
    english = models.CharField(max_length=250, default='')
    kana = models.CharField(max_length=250, default='')
    literal = models.CharField(max_length=250, default='', blank=True)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)
    kana_clean = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.kana_all_blank = re.sub(r'[^　。、？！]', "＿", self.kana)
        sentence_split = self.kana.split('　')
        sep = '　'
        for index, segment in enumerate(sentence_split):
            if index % 2 == 0:
                sentence_split[index] = re.sub(r'[^　。、？！]', "＿", segment)
        sentence_alt = sep.join(sentence_split)
        self.kana_alt_blank = sentence_alt
        self.kana_clean = re.sub(r'[　。、？！「」]', "", self.kana)
        super(DemoSentence, self).save(*args, **kwargs)


class DemoVocab(models.Model):
    english = models.CharField(max_length=250, unique=True, blank=False)
    kana = models.CharField(max_length=250, blank=False)
    kana_clean = models.CharField(max_length=250, blank=True)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.kana_all_blank = re.sub(r'[^　。、？！]', "＿", self.kana)
        alt_blank = ''
        count = 0
        for k in self.kana:
            if count % 2 == 0:
                alt_blank += k
            else:
                alt_blank += '＿'
            count += 1
        self.kana_alt_blank = alt_blank
        self.kana_clean = re.sub(r'[　。、？！「」\s]', "", self.kana)
        super(DemoVocab, self).save(*args, **kwargs)


class DemoExpression(models.Model):
    english = models.CharField(max_length=250, unique=True, blank=False)
    kana = models.CharField(max_length=250, blank=False)
    prompt = models.CharField(max_length=250, unique=False, blank=True)
    kana_clean = models.CharField(max_length=250, blank=True)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)
    note = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.kana_all_blank = re.sub(r'[^　。、？！]', "＿", self.kana)
        alt_blank = ''
        count = 0
        for k in self.kana:
            if count % 2 == 0:
                alt_blank += k
            else:
                alt_blank += '＿'
            count += 1
        self.kana_alt_blank = alt_blank
        self.kana_clean = re.sub(r'[　。、？！「」\s]', "", self.kana)
        super(DemoExpression, self).save(*args, **kwargs)


class DemoPractice(models.Model):
    pone_english = models.CharField(max_length=250, default='')
    ptwo_english = models.CharField(max_length=250, default='')
    pone_kana = models.CharField(max_length=250, default='')
    ptwo_kana = models.CharField(max_length=250, default='')
    pone_literal = models.CharField(max_length=250, default='', blank=True)
    ptwo_literal = models.CharField(max_length=250, default='', blank=True)
    vieworder = models.PositiveSmallIntegerField(default=1)
    pone_kana_clean = models.CharField(max_length=250, blank=True)
    ptwo_kana_clean = models.CharField(max_length=250, blank=True)
    pone_kana_all = models.CharField(max_length=250, blank=True)
    ptwo_kana_all = models.CharField(max_length=250, blank=True)
    pone_kana_alt = models.CharField(max_length=250, blank=True)
    ptwo_kana_alt = models.CharField(max_length=250, blank=True)

    @staticmethod
    def alt_practice_blanks(practice_kana, indexalt):
        practice_split = practice_kana.split('　')
        sep = '　'
        for index, segment in enumerate(practice_split):
            if indexalt is True:
                if index % 2 == 0:
                    practice_split[index] = re.sub(r'[^　。、？！]', "＿", segment)
            else:
                if index % 2 != 0:
                    practice_split[index] = re.sub(r'[^　。、？！]', "＿", segment)
        practice_hint = sep.join(practice_split)
        return practice_hint

    def save(self, *args, **kwargs):
        self.pone_kana_clean = re.sub(r'[　。、？！「」]', "", self.pone_kana)
        self.ptwo_kana_clean = re.sub(r'[　。、？！「」]', "", self.ptwo_kana)
        self.pone_kana_all = re.sub(r'[^　。、？！]', "＿", self.pone_kana)
        self.ptwo_kana_all = re.sub(r'[^　。、？！]', "＿", self.ptwo_kana)
        self.pone_kana_alt = DemoPractice.alt_practice_blanks(self.pone_kana, True)
        self.ptwo_kana_alt = DemoPractice.alt_practice_blanks(self.ptwo_kana, False)
        super(DemoPractice, self).save(*args, **kwargs)

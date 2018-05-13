import re
from django.db import models
from main.models import clean_sentence, all_blanks, hw_punctuation, create_blanks, create_splits


class BetaEmail(models.Model):
    user_beta_email = models.EmailField(max_length=50, unique=True)
    user_beta_submitted = models.DateTimeField(auto_now_add=True, blank=True)


class DemoSentence(models.Model):
    english = models.CharField(max_length=250, blank=False)
    kana = models.CharField(max_length=250, blank=False)
    f_kana = models.CharField(max_length=250, blank=True)
    literal = models.CharField(max_length=250, blank=True)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)
    kana_clean = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.kana = hw_punctuation(self.kana)
        self.kana_all_blank, self.kana_alt_blank, self.kana_clean = create_blanks(self.kana, 0, False)
        self.f_kana = create_splits(self.kana)
        self.kana_all_blank = create_splits(self.kana_all_blank)
        self.kana_alt_blank = create_splits(self.kana_alt_blank)
        super(DemoSentence, self).save(*args, **kwargs)


class DemoVocab(models.Model):
    english = models.CharField(max_length=250, unique=True, blank=False)
    kana = models.CharField(max_length=250, blank=False)
    f_kana = models.CharField(max_length=250, blank=True)
    kanji = models.CharField(max_length=250, blank=False)
    f_kanji = models.CharField(max_length=250, blank=True)
    kana_clean = models.CharField(max_length=250, blank=True)
    note = models.CharField(max_length=250, blank=True)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.kana = hw_punctuation(self.kana)
        self.kanji = hw_punctuation(self.kanji)
        self.kana_all_blank = all_blanks(self.kana)
        alt_blank = ''
        count = 0
        for k in self.kana:
            if count % 2 == 0:
                alt_blank += k
            else:
                alt_blank += '＿'
            count += 1
        self.kana_alt_blank = alt_blank
        self.kana_clean = clean_sentence(self.kana)
        self.f_kana = create_splits(self.kana)
        self.f_kanji = create_splits(self.kanji)
        self.kana_all_blank = create_splits(self.kana_all_blank)
        self.kana_alt_blank = create_splits(self.kana_alt_blank)
        super(DemoVocab, self).save(*args, **kwargs)


class DemoExpression(models.Model):
    english = models.CharField(max_length=250, unique=True, blank=False)
    kana = models.CharField(max_length=250, blank=False)
    f_kana = models.CharField(max_length=250, blank=True)
    prompt = models.CharField(max_length=250, blank=True)
    kana_clean = models.CharField(max_length=250, blank=True)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)
    note = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.kana = hw_punctuation(self.kana)
        self.kana_all_blank, self.kana_alt_blank, self.kana_clean = create_blanks(self.kana, 0, False)
        self.f_kana = create_splits(self.kana)
        self.kana_all_blank = create_splits(self.kana_all_blank)
        self.kana_alt_blank = create_splits(self.kana_alt_blank)
        super(DemoExpression, self).save(*args, **kwargs)


class DemoPractice(models.Model):
    pone_english = models.CharField(max_length=250, blank=False)
    ptwo_english = models.CharField(max_length=250, blank=False)
    pone_kana = models.CharField(max_length=250, blank=False)
    ptwo_kana = models.CharField(max_length=250, blank=False)
    pone_kana_f = models.CharField(max_length=250, blank=True)
    ptwo_kana_f = models.CharField(max_length=250, blank=True)
    pone_literal = models.CharField(max_length=250, blank=True)
    ptwo_literal = models.CharField(max_length=250, blank=True)
    vieworder = models.PositiveSmallIntegerField(default=1)
    pone_kana_clean = models.CharField(max_length=250, blank=True)
    ptwo_kana_clean = models.CharField(max_length=250, blank=True)
    pone_kana_all = models.CharField(max_length=250, blank=True)
    ptwo_kana_all = models.CharField(max_length=250, blank=True)
    pone_kana_alt = models.CharField(max_length=250, blank=True)
    ptwo_kana_alt = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.pone_kana = hw_punctuation(self.pone_kana)
        self.ptwo_kana = hw_punctuation(self.ptwo_kana)
        self.pone_kana_all, self.pone_kana_alt, self.pone_kana_clean = create_blanks(self.pone_kana, 0, True)
        self.ptwo_kana_all, self.ptwo_kana_alt, self.ptwo_kana_clean = create_blanks(self.ptwo_kana, 0, False)
        self.pone_kana_f = create_splits(self.pone_kana)
        self.ptwo_kana_f = create_splits(self.ptwo_kana)
        self.pone_kana_all = create_splits(self.pone_kana_all)
        self.pone_kana_alt = create_splits(self.pone_kana_alt)
        self.ptwo_kana_all = create_splits(self.ptwo_kana_all)
        self.ptwo_kana_alt = create_splits(self.ptwo_kana_alt)
        super(DemoPractice, self).save(*args, **kwargs)

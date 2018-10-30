import re
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from model_utils.managers import InheritanceManager
from pygments import highlight
from pygments.lexers import KairozuLexer
from pygments.formatters import KairozuFormatter


def create_context(sentence):
    whowhat = sentence[sentence.find("(") + 1:sentence.find(")")].lower()
    if whowhat == 'it' and (('half past' in sentence) or ('clock' in sentence) or ('PM' in sentence) or ('AM' in sentence) or (':' in sentence)):
        context = "Listener understands you're referring to the time."
    elif whowhat == 'it':
        context = "Listener can infer what 'it' is from the context of the conversation."
    elif whowhat == 'he' or whowhat == 'his':
        context = "Listener can infer who 'he' is from the context of the conversation."
    elif whowhat == 'she' or whowhat == 'her':
        context = "Listener can infer who 'she' is from the context of the conversation."
    elif whowhat == 'they' or whowhat == 'their' or whowhat == 'them':
        context = "Listener can infer who 'they' are from the context of the conversation."
    elif whowhat == 'i':
        context = "Listener understands you're referring to yourself from the context of the conversation."
    elif whowhat == 'my':
        context = "Listener can infer someone/thing is yours from the context of the conversation."
    elif whowhat == 'you' and sentence.startswith('Would') and sentence.endswith('?'):
        context = "Listener understands you're extending an invitation from the context of the conversation."
    elif whowhat == 'you' and sentence.endswith('?'):
        context = "Listener understands you're asking them from the context of the conversation."
    elif whowhat == 'you':
        context = "Listener understands you're referring to them from the context of the conversation."
    elif sentence.endswith('?') and (whowhat == 'your' or whowhat == 'yours'):
        context = "Listener understands you're asking about someone/thing related to them from the context of the conversation."
    elif whowhat == 'your' or whowhat == 'yours':
        context = "Listener understands you're referring to someone/thing related to them from the context of the conversation."
    elif whowhat == 'we' and "shall" not in sentence.lower():
        context = "Listener understands to whom you're referring from the context of the conversation."
    elif whowhat == 'we' and "shall" in sentence.lower():
        context = "You're asking the listener about a proposed plan of action."
    elif whowhat == 'our':
        context = "Listener understands to whom someone/thing belongs from the context of the conversation."
    elif whowhat == 'the color':
        context = "You are indicating color as an attribute; use the noun form of the color."
    else:
        context = ''
    return context

def clean_sentence(kana):
    cleaned = re.sub(r'[　｡。、､？?！!「」｢｣\s]', "", kana)
    return cleaned


def all_blanks(kana):
    all_blank = re.sub(r'[^　｡。、､？?！!「」｢｣\s]', "＿", kana)
    return all_blank


def hw_punctuation(hwtext):
    hwtext = re.sub(r'。', '｡　', hwtext)
    hwtext = re.sub(r'、[ 　]*', '､　', hwtext)
    hwtext = re.sub(r'[ 　]+', '　', hwtext)
    hwtext = hwtext.rstrip()
    return hwtext


def hw_single(hwtext):
    hwtext = re.sub(r'。', '｡ ', hwtext)
    hwtext = re.sub(r'、[ 　]*', '､ ', hwtext)
    hwtext = re.sub(r'[ 　]+', ' ', hwtext)
    hwtext = hwtext.rstrip()
    return hwtext


def disamb_all_blanks(kana, disamb_location):        # position 0 = disamb_loc 1
    disamb_split = kana.split('　')
    sep = '　'
    for index, segment in enumerate(disamb_split):
        if index == disamb_location - 1:
            disamb_split[index] = segment
        else:
            disamb_split[index] = all_blanks(segment)
    disamb = sep.join(disamb_split)
    return disamb


def create_blanks(kana, disamb_location, altindex):
    sentence_split = kana.split('　')
    sep = '　'

    if disamb_location > 0:
        kana_all_blank = disamb_all_blanks(kana, disamb_location)
    else:
        kana_all_blank = all_blanks(kana)

    for index, segment in enumerate(sentence_split):
        if altindex is True:
            if index % 2 == 0 and index != disamb_location - 1:
                sentence_split[index] = all_blanks(segment)
        else:
            if index % 2 != 0 and index != disamb_location - 1:
                sentence_split[index] = all_blanks(segment)

    kana_alt_blank = sep.join(sentence_split)
    kana_clean = clean_sentence(kana)
    return kana_all_blank, kana_alt_blank, kana_clean


def create_splits(splitme):
    splitme = re.sub(r'　', '　<wbr>', splitme)
    return splitme


class Profile(models.Model):
    """track and update user progress"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emailconfirmed = models.BooleanField(default=False)
    strictmode = models.BooleanField(default=False)
    preferkanji = models.BooleanField(default=False)
    frcount = models.PositiveIntegerField(default=0)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            FlashcardSet.objects.create(user=instance, name="default", description="Flashcards without an assigned set.")
            # VocabRecord.objects.initial_vocab_record(user=instance)
            instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        # VocabRecord.objects.initial_vocab_record(user=instance)
        instance.profile.save()

    @staticmethod
    def has_reviews(user):
        """check to see if a user has any pending reviews, and if so, how many"""
        now = timezone.now()
        user.profile.frcount = Flashcard.objects.filter(user_id=user.id, next_review__lte=now).count()
        fsets = FlashcardSet.objects.filter(user_id=user.id)
        for fset in fsets:
            fset.update_fsrcount()
        user.profile.save()


class BetaEmail(models.Model):
    user_beta_email = models.EmailField(max_length=50, unique=True)
    user_beta_submitted = models.DateTimeField(auto_now_add=True, blank=True)


class Chapter(models.Model):
    title = models.CharField(max_length=254, unique=True, blank=False)
    subtitle = models.CharField(max_length=254, blank=False)
    ALPHA = 'A'
    BETA = 'B'
    PUBLIC = 'P'
    HIDDEN = 'H'
    CHAPTER_STATUS_CHOICES = (
        (ALPHA, 'In Development'),
        (BETA, 'Beta Testing'),
        (PUBLIC, 'Public'),
        (HIDDEN, 'Hidden')
    )
    status = models.CharField(max_length=1, choices=CHAPTER_STATUS_CHOICES, default=ALPHA, blank=False)
    season = models.CharField(max_length=5, default='SXCX')

    class Meta:
        ordering = ['season']

    def __str__(self):
        return self.title


class Vocabulary(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, blank=False, null=False)
    english = models.CharField(max_length=250, blank=False)
    katakana = models.BooleanField(default=False)
    context = models.CharField(max_length=250, blank=True)
    kana = models.CharField(max_length=250, blank=False)
    kanji = models.CharField(max_length=250, unique=True, blank=False)
    kana_clean = models.CharField(max_length=250, blank=True)
    kanji_clean = models.CharField(max_length=250, blank=True)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kanji_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)
    kanji_alt_blank = models.CharField(max_length=250, blank=True)
    f_kana = models.CharField(max_length=250, blank=True)
    f_kanji = models.CharField(max_length=250, blank=True)

    UNCLASSIFIED = 0
    NOUN = 1
    VERB = 2
    ADJECTIVE = 3
    PRONOUN = 4
    ADVERB = 5
    PARTICLE = 6
    CONJUNCTION = 7
    COUNTER = 8
    INTERJECTION = 9
    INTERROGATIVE = 10
    EXPRESSION = 11
    NUMERIC = 12
    TEMPORAL = 13
    OTHER = 14
    PREFIX = 15
    SUFFIX = 16

    IADJ = 17
    NAADJ = 18
    NOADJ = 19

    RUVERB = 20
    UVERB = 21
    IRVERB = 22

    PARTOFSPEECH_CHOICES = (
        (UNCLASSIFIED, 'Unclassified'),
        (NOUN, 'Noun'),
        (VERB, 'Verb'),
        (ADJECTIVE, 'Adjective'),
        (PRONOUN, 'Pronoun'),
        (ADVERB, 'Adverb'),
        (PARTICLE, 'Particle'),
        (CONJUNCTION, 'Conjunction'),
        (COUNTER, 'Counter'),
        (INTERJECTION, 'Interjection'),
        (INTERROGATIVE, 'Interrogative'),
        (EXPRESSION, 'Expression'),
        (NUMERIC, 'Numeric'),
        (TEMPORAL, 'Temporal'),
        (PREFIX, 'Prefix'),
        (SUFFIX, 'Suffix'),
        (OTHER, 'Other'),
        (IADJ, 'i-Adjective'),
        (NAADJ, 'na-Adjective'),
        (NOADJ, 'no-Adjective'),
        (RUVERB, 'ru-Verb v1'),
        (UVERB, 'u-Verb v5'),
        (IRVERB, 'irreg verb')
    )
    partofspeech = models.PositiveSmallIntegerField(choices=PARTOFSPEECH_CHOICES, default=UNCLASSIFIED, blank=False, null=False)

    def save(self, *args, **kwargs):
        self.kana = hw_punctuation(self.kana)
        self.kanji = hw_punctuation(self.kanji)
        self.kana_all_blank = all_blanks(self.kana)
        self.kanji_all_blank = all_blanks(self.kanji)
        alt_blank = ''
        count = 0
        for k in self.kana:
            if count % 2 == 0:
                alt_blank += k
            else:
                alt_blank += '＿'
            count += 1
        alt_blank_kanji = ''
        count_kanji = 0
        for j in self.kanji:
            if count_kanji % 2 == 0:
                alt_blank_kanji += j
            else:
                alt_blank_kanji += '＿'
            count_kanji += 1
        self.kana_alt_blank = alt_blank
        self.kanji_alt_blank = alt_blank_kanji
        self.kana_clean = clean_sentence(self.kana)
        self.kanji_clean = clean_sentence(self.kanji)
        self.f_kana = create_splits(self.kana)
        self.f_kanji = create_splits(self.kanji)
        self.kana_alt_blank = create_splits(self.kana_alt_blank)
        self.kanji_alt_blank = create_splits(self.kanji_alt_blank)
        self.kana_all_blank = create_splits(self.kana_all_blank)
        self.kanji_all_blank = create_splits(self.kanji_all_blank)
        super(Vocabulary, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "vocabularies"

    def __unicode__(self):
        return self.english


class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=254, unique=True)
    english = models.CharField(max_length=254, unique=True, blank=False)
    hiragana = models.CharField(max_length=254, unique=True, blank=False)
    overview = models.TextField(blank=True)
    point_active = models.BooleanField(default=True)
    f_english = models.CharField(max_length=254, blank=True)
    f_hiragana = models.CharField(max_length=254, blank=True)

    def lesson_pieces(self):
        pieces_by_displayorder = Piece.objects.filter(lesson_id__in=[self.id]).select_subclasses().order_by('displayorder')
        return pieces_by_displayorder

    def save(self, *args, **kwargs):
        self.hiragana = hw_punctuation(self.hiragana)
        self.overview = hw_single(self.overview)
        self.f_english = highlight(self.english, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_hiragana = highlight(self.hiragana, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_hiragana = create_splits(self.f_hiragana)
        super(Lesson, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['chapter', 'id']


class PointTable(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='points', on_delete=models.CASCADE, blank=False, null=False)
    pointa = models.CharField(max_length=500, blank=True)
    pointb = models.CharField(max_length=500, blank=True)
    f_pointa = models.CharField(max_length=500, blank=True)
    f_pointb = models.CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        self.f_pointa = highlight(self.pointa, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_pointb = highlight(self.pointb, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_pointa = re.sub('。', '｡', self.f_pointa)
        self.f_pointa = re.sub('、[ 　]*', '､ ', self.f_pointa)
        self.f_pointb = re.sub('。', '｡', self.f_pointb)
        self.f_pointb = re.sub('、[ 　]*', '､ ', self.f_pointb)
        super(PointTable, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']


class Piece(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=False, null=False)
    displayorder = models.PositiveSmallIntegerField(default=0)
    objects = InheritanceManager()

    class Meta:
        ordering = ['lesson', 'displayorder']


class DivBlock(Piece):
    shape = models.PositiveSmallIntegerField(default=0, editable=False)
    text = models.TextField(blank=True)
    f_text = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.f_text = highlight(self.text, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        super(DivBlock, self).save(*args, **kwargs)


class Block(Piece):
    shape = models.PositiveSmallIntegerField(default=1, editable=False)
    text = models.TextField(blank=True)
    f_text = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.f_text = highlight(self.text, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        super(Block, self).save(*args, **kwargs)


class TwoTable(Piece):
    shape = models.PositiveSmallIntegerField(default=2, editable=False)
    title = models.CharField(max_length=254, blank=True)
    header = models.BooleanField(default=False)
    head_prea = models.CharField(max_length=254, blank=True)
    head_posta = models.CharField(max_length=254, blank=True)
    head_note = models.CharField(max_length=254, blank=True)


class TwoTableData(models.Model):
    owner = models.ForeignKey(TwoTable, on_delete=models.CASCADE, blank=False, null=False)
    prea = models.CharField(max_length=254, blank=True)
    posta = models.CharField(max_length=254, blank=True)
    note = models.CharField(max_length=254, blank=True)
    f_prea = models.CharField(max_length=512, blank=True)
    f_posta = models.CharField(max_length=512, blank=True)
    f_note = models.CharField(max_length=512, blank=True)

    def save(self, *args, **kwargs):
        self.f_prea = highlight(self.prea, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_posta = highlight(self.posta, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_note = highlight(self.note, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        super(TwoTableData, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']

class FourTable(Piece):
    shape = models.PositiveSmallIntegerField(default=4, editable=False)
    title = models.CharField(max_length=254, blank=True)
    header = models.BooleanField(default=False)
    center = models.BooleanField(default=True)
    arrow = models.BooleanField(default=True)
    head_prea = models.CharField(max_length=254, blank=True)
    head_preb = models.CharField(max_length=254, blank=True)
    head_prec = models.CharField(max_length=254, blank=True)
    head_posta = models.CharField(max_length=254, blank=True)
    head_postb = models.CharField(max_length=254, blank=True)
    head_postc = models.CharField(max_length=254, blank=True)


class FourTableData(models.Model):
    owner = models.ForeignKey(FourTable, on_delete=models.CASCADE, blank=False, null=False)
    prea = models.CharField(max_length=254, blank=True)
    preb = models.CharField(max_length=254, blank=True)
    prec = models.CharField(max_length=254, blank=True)
    posta = models.CharField(max_length=254, blank=True)
    postb = models.CharField(max_length=254, blank=True)
    postc = models.CharField(max_length=254, blank=True)
    f_prea = models.CharField(max_length=512, blank=True)
    f_preb = models.CharField(max_length=512, blank=True)
    f_prec = models.CharField(max_length=512, blank=True)
    f_posta = models.CharField(max_length=512, blank=True)
    f_postb = models.CharField(max_length=512, blank=True)
    f_postc = models.CharField(max_length=512, blank=True)

    def save(self, *args, **kwargs):
        self.f_prea = highlight(self.prea, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_preb = highlight(self.preb, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_prec = highlight(self.prec, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_posta = highlight(self.posta, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_postb = highlight(self.postb, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.f_postc = highlight(self.postc, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        super(FourTableData, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']

class Example(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='examples', on_delete=models.CASCADE, blank=False, null=False)
    english = models.CharField(max_length=254, unique=True, blank=True)
    hiragana = models.CharField(max_length=254, unique=True, blank=True)
    f_english = models.CharField(max_length=512, blank=True)
    f_hiragana = models.CharField(max_length=512, blank=True)

    def save(self, *args, **kwargs):
        self.f_english = highlight(self.english, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        self.hiragana = hw_single(self.hiragana)
        self.f_hiragana = highlight(self.hiragana, KairozuLexer(ensurenl=False), KairozuFormatter(style='kairozu'))
        super(Example, self).save(*args, **kwargs)


class MoreInfo(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='moreinfos', on_delete=models.CASCADE, blank=False, null=False)
    text = models.TextField(blank=True)


class InfoLink(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='infolinks', on_delete=models.CASCADE, blank=False, null=False)
    linkname = models.CharField(max_length=50, unique=False, blank=True)
    linkurl = models.URLField(max_length=256, unique=False, blank=True)
    linkdesc = models.CharField(max_length=256, unique=False, blank=True)


class Practice(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=False, null=False)
    strict = models.BooleanField(default=False)
    pone_english = models.CharField(max_length=250, blank=False)
    ptwo_english = models.CharField(max_length=250, blank=False)
    pone_kana = models.CharField(max_length=250, blank=False)
    ptwo_kana = models.CharField(max_length=250, blank=False)
    pone_kanji = models.CharField(max_length=250, blank=False)
    ptwo_kanji = models.CharField(max_length=250, blank=False)
    pone_literal = models.CharField(max_length=250, blank=True)
    ptwo_literal = models.CharField(max_length=250, blank=True)
    pone_context = models.CharField(max_length=250, blank=True)
    ptwo_context = models.CharField(max_length=250, blank=True)
    pone_disamb_location = models.PositiveSmallIntegerField(default=0)
    ptwo_disamb_location = models.PositiveSmallIntegerField(default=0)
    vieworder = models.PositiveSmallIntegerField(default=1)
    pone_kana_clean = models.CharField(max_length=250, blank=True)
    ptwo_kana_clean = models.CharField(max_length=250, blank=True)
    pone_kanji_clean = models.CharField(max_length=250, blank=True)
    ptwo_kanji_clean = models.CharField(max_length=250, blank=True)
    pone_kana_all = models.CharField(max_length=250, blank=True)
    ptwo_kana_all = models.CharField(max_length=250, blank=True)
    pone_kanji_all = models.CharField(max_length=250, blank=True)
    ptwo_kanji_all = models.CharField(max_length=250, blank=True)
    pone_kana_alt = models.CharField(max_length=250, blank=True)
    ptwo_kana_alt = models.CharField(max_length=250, blank=True)
    pone_kanji_alt = models.CharField(max_length=250, blank=True)
    ptwo_kanji_alt = models.CharField(max_length=250, blank=True)
    pone_kana_f = models.CharField(max_length=250, blank=True)
    ptwo_kana_f = models.CharField(max_length=250, blank=True)
    pone_kanji_f = models.CharField(max_length=250, blank=True)
    ptwo_kanji_f = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if '(' in self.pone_english:
            self.pone_context = create_context(self.pone_english)
        if '(' in self.ptwo_english:
            self.ptwo_context = create_context(self.ptwo_english)

        self.pone_kana = hw_punctuation(self.pone_kana)
        self.ptwo_kana = hw_punctuation(self.ptwo_kana)
        self.pone_kanji = hw_punctuation(self.pone_kanji)
        self.ptwo_kanji = hw_punctuation(self.ptwo_kanji)
        self.pone_kana_all, self.pone_kana_alt, self.pone_kana_clean = create_blanks(self.pone_kana, self.pone_disamb_location, True)
        self.ptwo_kana_all, self.ptwo_kana_alt, self.ptwo_kana_clean = create_blanks(self.ptwo_kana, self.ptwo_disamb_location, False)
        self.pone_kanji_all, self.pone_kanji_alt, self.pone_kanji_clean = create_blanks(self.pone_kanji, self.pone_disamb_location, True)
        self.ptwo_kanji_all, self.ptwo_kanji_alt, self.ptwo_kanji_clean = create_blanks(self.ptwo_kanji, self.ptwo_disamb_location, False)
        self.pone_kana_f = create_splits(self.pone_kana)
        self.ptwo_kana_f = create_splits(self.ptwo_kana)
        self.pone_kanji_f = create_splits(self.pone_kanji)
        self.ptwo_kanji_f = create_splits(self.ptwo_kanji)
        self.pone_kana_all = create_splits(self.pone_kana_all)
        self.pone_kana_alt = create_splits(self.pone_kana_alt)
        self.pone_kanji_all = create_splits(self.pone_kanji_all)
        self.pone_kanji_alt = create_splits(self.pone_kanji_alt)
        self.ptwo_kana_all = create_splits(self.ptwo_kana_all)
        self.ptwo_kana_alt = create_splits(self.ptwo_kana_alt)
        self.ptwo_kanji_all = create_splits(self.ptwo_kanji_all)
        self.ptwo_kanji_alt = create_splits(self.ptwo_kanji_alt)
        super(Practice, self).save(*args, **kwargs)

    class Meta:
        ordering = ['lesson', 'vieworder']


class GrammarNote(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=254, unique=True)
    notetext = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['lesson', 'id']


class Sentence(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=False, null=False)
    strict = models.BooleanField(default=False)
    english = models.CharField(max_length=250, blank=False)
    kana = models.CharField(max_length=250, blank=False)
    kanji = models.CharField(max_length=250, blank=False)
    literal = models.CharField(max_length=250, blank=True)
    context = models.CharField(max_length=250, blank=True)
    disamb_location = models.PositiveSmallIntegerField(default=0)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kanji_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)
    kanji_alt_blank = models.CharField(max_length=250, blank=True)
    kana_clean = models.CharField(max_length=250, blank=True)
    kanji_clean = models.CharField(max_length=250, blank=True)
    f_kana = models.CharField(max_length=250, blank=True)
    f_kanji = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if '(' in self.english:
            self.context = create_context(self.english)

        self.kana = hw_punctuation(self.kana)
        self.kanji = hw_punctuation(self.kanji)
        self.kana_all_blank, self.kana_alt_blank, self.kana_clean = create_blanks(self.kana, self.disamb_location, False)
        self.kanji_all_blank, self.kanji_alt_blank, self.kanji_clean = create_blanks(self.kanji, self.disamb_location, False)
        self.f_kana = create_splits(self.kana)
        self.f_kanji = create_splits(self.kanji)
        self.kana_all_blank = create_splits(self.kana_all_blank)
        self.kanji_all_blank = create_splits(self.kanji_all_blank)
        self.kana_alt_blank = create_splits(self.kana_alt_blank)
        self.kanji_alt_blank = create_splits(self.kanji_alt_blank)
        super(Sentence, self).save(*args, **kwargs)

    class Meta:
        ordering = ['lesson']


class FlashcardSet(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=10, unique=True, blank=False, validators=[alphanumeric])
    fsrcount = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=20, unique=True)
    description = models.CharField(max_length=250, blank=False)

    def save(self, *args, **kwargs):
        self.slug = self.name + "-" + str(self.user.id)
        super(FlashcardSet, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cards = self.flashcard_set.all()
        defaultset = FlashcardSet.objects.filter(user_id__exact=self.user.id, name="default").first()
        for card in cards:
            card.set = defaultset
            card.save()
        super(FlashcardSet, self).delete(*args, **kwargs)

    def update_fsrcount(self, *args, **kwargs):
        now = timezone.now()
        self.fsrcount = self.flashcard_set.filter(next_review__lte=now).count()
        super(FlashcardSet, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    """adding user personalized study content"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    set = models.ForeignKey(FlashcardSet, on_delete=models.DO_NOTHING, blank=False, null=False)
    strict = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    english = models.CharField(max_length=250, blank=False)
    kana = models.CharField(max_length=250, blank=False)
    kanji = models.CharField(max_length=250, blank=True)
    literal = models.CharField(max_length=250, blank=True)
    context = models.CharField(max_length=250, blank=True)
    note = models.CharField(max_length=500, blank=True)
    disamb_location = models.PositiveSmallIntegerField(default=0)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)
    kana_clean = models.CharField(max_length=250, blank=True)
    kanji_all_blank = models.CharField(max_length=250, blank=True)
    kanji_alt_blank = models.CharField(max_length=250, blank=True)
    kanji_clean = models.CharField(max_length=250, blank=True)
    f_kana = models.CharField(max_length=250, blank=True)
    f_kanji = models.CharField(max_length=250, blank=True)
    next_review = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0)                          # number of consecutive corrects

    def save(self, *args, **kwargs):
        self.kana = hw_punctuation(self.kana)
        self.kanji = hw_punctuation(self.kanji)
        self.kana_all_blank, self.kana_alt_blank, self.kana_clean = create_blanks(self.kana, 0, False)
        self.kanji_all_blank, self.kanji_alt_blank, self.kanji_clean = create_blanks(self.kanji, 0, False)
        self.f_kana = create_splits(self.kana)
        self.f_kanji = create_splits(self.kanji)
        self.kana_all_blank = create_splits(self.kana_all_blank)
        self.kana_alt_blank = create_splits(self.kana_alt_blank)
        self.kanji_all_blank = create_splits(self.kanji_all_blank)
        self.kanji_alt_blank = create_splits(self.kanji_alt_blank)
        if not self.set:
            self.set = FlashcardSet.objects.filter(user_id__exact=self.user.id, name__exact="default").first()
        super(Flashcard, self).save(*args, **kwargs)

    class Meta:
        ordering = ['user']


@receiver(user_logged_in)
def update_vr_sr_counts(sender, user, request, **kwargs):
    Profile.has_reviews(user)

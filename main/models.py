import re
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from model_utils.managers import InheritanceManager
from model_utils import Choices
from pygments import highlight
from pygments.lexers import KairozuLexer
from pygments.formatters import KairozuFormatter


def create_context(sentence):
    whowhat = sentence[sentence.find("(") + 1:sentence.find(")")].lower()
    if whowhat == 'it' and 'half past' or 'clock' or 'PM' or 'AM' or ':' in sentence:
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
    currentchapter = models.PositiveSmallIntegerField(default=1)
    pendingchapter = models.PositiveSmallIntegerField(default=1)
    currentlesson = models.PositiveSmallIntegerField(default=1)
    currentpractice = models.PositiveSmallIntegerField(default=1)
    currentexpression = models.PositiveSmallIntegerField(default=1)
    currentexercise = models.PositiveSmallIntegerField(default=1)
    attemptexercise = models.PositiveSmallIntegerField(default=0)
    currentvocab = models.PositiveSmallIntegerField(default=1)
    currentstory = models.PositiveSmallIntegerField(default=1)
    strictmode = models.BooleanField(default=False)
    vrcount = models.PositiveIntegerField(default=0)
    srcount = models.PositiveIntegerField(default=0)
    ercount = models.PositiveIntegerField(default=0)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            VocabRecord.objects.initial_vocab_record(user=instance)
            SentenceRecord.objects.initial_sentence_record(user=instance)
            ExerciseRecord.objects.initial_exercise_record(user=instance)
            ExpressionRecord.objects.initial_expression_record(user=instance)
            instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        # Profile.objects.create(user=instance)
        instance.profile.save()

    # @receiver(post_save, sender=Profile)
    # def update_records(sender, instance, **kwargs):
    #     VocabRecord.objects.update_vocab_record(profile=instance)
    #     SentenceRecord.objects.update_sentence_record(profile=instance)
    #     ExerciseRecord.objects.update_exercise_record(profile=instance)
    #     ExpressionRecord.objects.update_expression_record(profile=instance)

    @staticmethod
    def ok_to_graduate(user):
        """check to see if user has too many pending reviews"""
        if user.profile.vrcount < 75 and user.profile.srcount < 100 and user.profile.ercount < 25:
            if Profile.chapter_mastery_level(user) > 80 and user.profile.pendingchapter == int(user.profile.currentchapter)+1:
                Profile.graduate_chapter(user, user.profile.currentchapter)

    @staticmethod
    def has_reviews(user):
        """check to see if a user has any pending reviews, and if so, how many"""
        now = timezone.now()
        user.profile.vrcount = VocabRecord.objects.filter(user_id=user.id, next_review__lte=now).count()
        user.profile.srcount = SentenceRecord.objects.filter(user_id=user.id, next_review__lte=now).count()
        user.profile.ercount = ExpressionRecord.objects.filter(user_id=user.id, next_review__lte=now).count()
        Profile.ok_to_graduate(user)
        user.profile.save()


    @staticmethod
    def chapter_mastery_level(user):
        vtotal = VocabRecord.objects.filter(user_id=user.id, rating__gt=0).count()
        vbeginner = VocabRecord.objects.filter(user_id=user.id, rating__gt=0, score__lte=2).count()
        stotal = SentenceRecord.objects.filter(user_id=user.id, rating__gt=0).count()
        sbeginner = SentenceRecord.objects.filter(user_id=user.id, rating__gt=0, score__lte=2).count()
        etotal = ExpressionRecord.objects.filter(user_id=user.id, rating__gt=0).count()
        ebeginner = ExpressionRecord.objects.filter(user_id=user.id, rating__gt=0, score__lte=2).count()
        if vtotal+stotal+etotal > 0:
            vmastery = int((1-((vbeginner+sbeginner+ebeginner)/(vtotal+stotal+etotal)))*100)
        else:
            vmastery = 0
        return vmastery

    @staticmethod
    def graduate_exercise(user, exercise_view):
        """increase user's current exercise to exercise_view+1 -- allows access to next exercise"""
        if user.profile.currentexercise == int(exercise_view):
            user.profile.currentexercise = int(exercise_view) + 1
        user.profile.save()

    @staticmethod
    def attempted_exercise(user, exercise_view):
        """if user has attempted an exercise, but not necessarily completed it successfully"""
        if user.profile.currentexercise == exercise_view:
            user.profile.attemptexercise = exercise_view
        user.profile.save()

    @staticmethod
    def graduate_vocab(user, chapter_id):
        """increase user's currentvocab to chapter.id+1 -- allows access to first lesson"""
        if user.profile.currentvocab == int(chapter_id):
            user.profile.currentvocab = int(chapter_id) + 1
        user.profile.save()
        VocabRecord.objects.update_vocab_record(profile=user.profile)

    @staticmethod
    def graduate_expression(user, chapter_id):
        """increase user's currentvocab to chapter.id+1 -- allows access to first lesson"""
        if user.profile.currentexpression == int(chapter_id):
            user.profile.currentexpression = int(chapter_id) + 1
        user.profile.save()
        ExpressionRecord.objects.update_expression_record(profile=user.profile)

    @staticmethod
    def graduate_chapter(user, chapter_id):
        """increase user's currentchapter to chapter.id+1 -- allows access to next chapter"""
        if user.profile.currentchapter == int(chapter_id):
            user.profile.currentchapter = int(chapter_id) + 1
        user.profile.save()
        ExerciseRecord.objects.update_exercise_record(profile=user.profile)

    @staticmethod
    def graduate_pending(user, chapter_id):
        """increase user's pendingchapter to chapter.id+1 -- allows grad to next chapter after reviews"""
        if user.profile.pendingchapter == int(chapter_id):
            user.profile.pendingchapter = int(chapter_id) + 1
        user.profile.save()

    @staticmethod
    def graduate_lesson(user, lesson_id):
        """increase user's currentlesson to lesson.id+1 -- allows access to next lesson"""
        currentlesson = Lesson.objects.get(id=lesson_id)    # Chapter.objects.get(id=chapter_id)
        currentchapter = currentlesson.chapter
        lastlesson = currentchapter.lesson_set.last()
        if int(lesson_id) == lastlesson.id:
            if user.profile.currentstory == currentchapter.id:
                user.profile.currentstory = currentchapter.id + 1
        if user.profile.currentlesson == lesson_id:
            user.profile.currentlesson = int(lesson_id) + 1
        user.profile.save()
        SentenceRecord.objects.update_sentence_record(profile=user.profile)

    @staticmethod
    def graduate_practice(user, lesson_id):
        """increase user's currentpractice to lesson.id+1 -- allows access to sentences"""
        if user.profile.currentpractice == int(lesson_id):
            user.profile.currentpractice = int(lesson_id) + 1
        user.profile.save()


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


class Expression(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, blank=False, null=False)
    english = models.CharField(max_length=250, blank=False)
    example = models.CharField(max_length=250, blank=True)
    literal = models.CharField(max_length=250, blank=True)
    katakana = models.BooleanField(default=False)
    context = models.CharField(max_length=250, blank=True)
    kana = models.CharField(max_length=250, blank=False)
    kanji = models.CharField(max_length=250, unique=True, blank=False)
    kana_clean = models.CharField(max_length=250, blank=True)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)
    f_kana = models.CharField(max_length=250, blank=True)
    f_kanji = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.kana = hw_punctuation(self.kana)
        self.kanji = hw_punctuation(self.kanji)
        self.kana_all_blank, self.kana_alt_blank, self.kana_clean = create_blanks(self.kana, 0, False)
        self.f_kana = create_splits(self.kana)
        self.f_kanji = create_splits(self.kanji)
        self.kana_all_blank = create_splits(self.kana_all_blank)
        self.kana_alt_blank = create_splits(self.kana_alt_blank)
        super(Expression, self).save(*args, **kwargs)


class ExpressionRecordManager(models.Manager):
    """create and manage expressionrecords for each user"""
    def update_expression_record(self, profile):
        userexpression = profile.currentexpression
        expressions = Expression.objects.filter(chapter_id__exact=userexpression)
        user = profile.user

        if not ExpressionRecord.objects.filter(user=user, express__chapter_id__exact=userexpression).exists() and len(expressions) > 0:
            for exp in expressions:
                self.create(user=user, express=exp)

    def initial_expression_record(self, user):   # create the vocab records for chapter 1 when user is created
        expressions = Expression.objects.filter(chapter_id__exact=1)

        if len(expressions) > 0:
            for exp in expressions:
                self.get_or_create(user=user, express=exp)


class ExpressionRecord(models.Model):
    """tracking user progress for each expression"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    express = models.ForeignKey(Expression, on_delete=models.CASCADE, blank=False, null=False)
    last_attempt = models.DateTimeField(default=timezone.now, blank=True)
    next_review = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    objects = ExpressionRecordManager()

    class Meta:
        ordering = ['next_review']


class Vocabulary(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, blank=False, null=False)
    english = models.CharField(max_length=250, blank=False)
    katakana = models.BooleanField(default=False)
    context = models.CharField(max_length=250, blank=True)
    kana = models.CharField(max_length=250, blank=False)
    kanji = models.CharField(max_length=250, unique=True, blank=False)
    kana_clean = models.CharField(max_length=250, blank=True)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)
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
        self.kana_alt_blank = create_splits(self.kana_alt_blank)
        self.kana_all_blank = create_splits(self.kana_all_blank)
        super(Vocabulary, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "vocabularies"

    def __unicode__(self):
        return self.english


class VocabRecordManager(models.Manager):
    """create and manage vocabrecords for each user"""
    def update_vocab_record(self, profile):
        uservocab = profile.currentvocab
        vocabularies = Vocabulary.objects.filter(chapter_id__exact=uservocab)
        user = profile.user

        if not VocabRecord.objects.filter(user=user, vocab__chapter_id__exact=uservocab).exists() and len(vocabularies) > 0:
            for voc in vocabularies:
                self.create(user=user, vocab=voc)

    def initial_vocab_record(self, user):   # create the vocab records for chapter 1 when user is created
        vocabularies = Vocabulary.objects.filter(chapter_id__exact=1)

        if len(vocabularies) > 0:
            for voc in vocabularies:
                self.get_or_create(user=user, vocab=voc)


class VocabRecord(models.Model):
    """tracking user progress for each vocabulary word"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    vocab = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, blank=False, null=False)
    last_attempt = models.DateTimeField(default=timezone.now, blank=True)
    next_review = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    rating = models.PositiveSmallIntegerField(default=0)
    objects = VocabRecordManager()

    class Meta:
        ordering = ['next_review']


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
    pone_kana_all = models.CharField(max_length=250, blank=True)
    ptwo_kana_all = models.CharField(max_length=250, blank=True)
    pone_kana_alt = models.CharField(max_length=250, blank=True)
    ptwo_kana_alt = models.CharField(max_length=250, blank=True)
    pone_kana_f = models.CharField(max_length=250, blank=True)
    ptwo_kana_f = models.CharField(max_length=250, blank=True)
    pone_kanji_f = models.CharField(max_length=250, blank=True)
    ptwo_kanji_f = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if '(' in self.pone_english:
            self.pone_context = create_context(self.pone_english)
        if '(' in self.ptwo_english:
            self.ptwo_context = create_context(self.ptwo_english)

        if self.force_strict == 1:
            self.strict = True
        else:
            self.strict = False
        self.pone_kana = hw_punctuation(self.pone_kana)
        self.ptwo_kana = hw_punctuation(self.ptwo_kana)
        self.pone_kanji = hw_punctuation(self.pone_kanji)
        self.ptwo_kanji = hw_punctuation(self.ptwo_kanji)
        self.pone_kana_all, self.pone_kana_alt, self.pone_kana_clean = create_blanks(self.pone_kana, self.pone_disamb_location, True)
        self.ptwo_kana_all, self.ptwo_kana_alt, self.ptwo_kana_clean = create_blanks(self.ptwo_kana, self.ptwo_disamb_location, False)
        self.pone_kana_f = create_splits(self.pone_kana)
        self.ptwo_kana_f = create_splits(self.ptwo_kana)
        self.pone_kanji_f = create_splits(self.pone_kanji)
        self.ptwo_kanji_f = create_splits(self.ptwo_kanji)
        self.pone_kana_all = create_splits(self.pone_kana_all)
        self.pone_kana_alt = create_splits(self.pone_kana_alt)
        self.ptwo_kana_all = create_splits(self.ptwo_kana_all)
        self.ptwo_kana_alt = create_splits(self.ptwo_kana_alt)
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


class Exercise(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, blank=False, null=False)
    description = models.CharField(max_length=250, default='', blank=True)
    exercise_order = models.PositiveSmallIntegerField(default=1)
    EXERCISE_TYPE_CHOICES = Choices('passage', 'dialogue')
    exercise_type = models.CharField(choices=EXERCISE_TYPE_CHOICES, default=EXERCISE_TYPE_CHOICES.passage, max_length=10)
    exercise_word = models.CharField(max_length=25, default='')

    def exercise_pieces(self):
        pieces_by_displayorder = ExercisePiece.objects.filter(exercise_id__in=[self.id]).select_subclasses(ExercisePrompt)
        return pieces_by_displayorder

    @staticmethod
    def exercise_pieces_admin_prompt(chapter_id):
        prompt_admin = ExercisePiece.objects.filter(exercise__chapter__id__in=chapter_id).select_subclasses(ExercisePrompt)
        return prompt_admin

    @staticmethod
    def exercise_pieces_admin_sentence(chapter_id):
        sentence_admin = ExercisePiece.objects.filter(exercise__chapter__id__in=chapter_id).select_subclasses(ExercisePrompt)
        return sentence_admin

    class Meta:
        ordering = ['exercise_order']


class ExercisePiece(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, blank=False, null=False)
    objects = InheritanceManager()

    class Meta:
        ordering = ['exercise']


class ExerciseSentence(ExercisePiece):
    display_order = models.PositiveSmallIntegerField(default=1)
    english = models.CharField(max_length=250, blank=False)
    kana = models.CharField(max_length=250, blank=False)
    kanji = models.CharField(max_length=250, blank=False)
    literal = models.CharField(max_length=250, blank=True)
    context = models.CharField(max_length=250, blank=True)
    disamb_location = models.PositiveSmallIntegerField(default=0)
    kana_all_blank = models.CharField(max_length=250, blank=True)
    kana_alt_blank = models.CharField(max_length=250, blank=True)
    kana_clean = models.CharField(max_length=250, blank=True)
    f_kana = models.CharField(max_length=250, blank=True)
    f_kanji = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if '(' in self.english:
            self.context = create_context(self.english)

        self.kana = hw_punctuation(self.kana)
        self.kanji = hw_punctuation(self.kanji)
        self.kana_all_blank, self.kana_alt_blank, self.kana_clean = create_blanks(self.kana, self.disamb_location, False)
        self.f_kana = create_splits(self.kana)
        self.f_kanji = create_splits(self.kanji)
        self.kana_alt_blank = create_splits(self.kana_alt_blank)
        self.kana_all_blank = create_splits(self.kana_all_blank)
        super(ExerciseSentence, self).save(*args, **kwargs)

    class Meta:
        ordering = ['display_order']


class ExercisePrompt(ExercisePiece):
    prompt_name = models.CharField(max_length=250, blank=False)
    prompt_order = models.PositiveSmallIntegerField(default=1)
    prompt_kana = models.CharField(max_length=250, blank=False)
    prompt_kana_f = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.prompt_kana = hw_punctuation(self.prompt_kana)
        self.prompt_kana_f = create_splits(self.prompt_kana)
        super(ExercisePrompt, self).save(*args, **kwargs)

    class Meta:
        ordering = ['prompt_order']


class ExerciseResponse(models.Model):
    exercise_prompt = models.ForeignKey(ExercisePrompt, related_name='responses', on_delete=models.CASCADE, blank=False, null=False)
    response_order = models.PositiveSmallIntegerField(default=1)
    response_english = models.CharField(max_length=250, blank=False)
    response_kana = models.CharField(max_length=250, blank=False)
    response_kanji = models.CharField(max_length=250, blank=False)
    response_literal = models.CharField(max_length=250, blank=True)
    response_context = models.CharField(max_length=250, blank=True)
    response_disamb_location = models.PositiveSmallIntegerField(default=0)
    response_kana_all_blank = models.CharField(max_length=250, blank=True)
    response_kana_alt_blank = models.CharField(max_length=250, blank=True)
    response_kana_clean = models.CharField(max_length=250, blank=True)
    response_kana_f = models.CharField(max_length=250, blank=True)
    response_kanji_f = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ['exercise_prompt', 'response_order']

    def save(self, *args, **kwargs):
        if '(' in self.response_english:
            self.response_context = create_context(self.response_english)

        self.response_kana = hw_punctuation(self.response_kana)
        self.response_kanji = hw_punctuation(self.response_kanji)
        self.response_kana_all_blank, self.response_kana_alt_blank, self.response_kana_clean = create_blanks(self.response_kana, self.response_disamb_location, False)
        self.response_kana_f = create_splits(self.response_kana)
        self.response_kanji_f = create_splits(self.response_kanji)
        self.response_kana_alt_blank = create_splits(self.response_kana_alt_blank)
        self.response_kana_all_blank = create_splits(self.response_kana_all_blank)
        super(ExerciseResponse, self).save(*args, **kwargs)


class ExerciseRecordManager(models.Manager):
    def update_exercise_record(self, profile):
        userstory = profile.currentstory
        exercises = Exercise.objects.filter(chapter_id__exact=userstory)
        user = profile.user

        if len(exercises) > 0:
            for exer in exercises:
                self.get_or_create(user=user, exercise=exer)

    def initial_exercise_record(self, user):
        exercises = Exercise.objects.filter(chapter_id__exact=1)

        if len(exercises) > 0:
            for exer in exercises:
                self.get_or_create(user=user, exercise=exer)


class ExerciseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, blank=False, null=False)
    last_attempt = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0.0)
    rating = models.PositiveSmallIntegerField(default=0)
    objects = ExerciseRecordManager()

    class Meta:
        ordering = ['user', 'last_attempt']

    @staticmethod
    def check_chapter_exercises(user, chapter_id):
        exerciserecord_check = ExerciseRecord.objects.filter(user_id=user.id, exercise__chapter__id=chapter_id, rating__lt=2).first()
        if exerciserecord_check is None and user.profile.pendingchapter == chapter_id:
            Profile.graduate_pending(user, chapter_id)
            Profile.ok_to_graduate(user)

    @staticmethod
    def update_grade(exerciserecord_id, exercise_grade, user):
        grade = float(exercise_grade)
        exerciserecord = ExerciseRecord.objects.get(id=exerciserecord_id)
        exerciserecord.last_attempt = timezone.now()
        exerciserecord.score = grade
        if grade >= 0.98:
            exerciserecord.rating = 3
            Profile.graduate_exercise(user, exerciserecord.exercise.exercise_order)
        elif grade >= 0.70:
            exerciserecord.rating = 2
            Profile.graduate_exercise(user, exerciserecord.exercise.exercise_order)
        else:
            exerciserecord.rating = 1
            Profile.attempted_exercise(user, exerciserecord.exercise.exercise_order)
        exerciserecord.save()
        ExerciseRecord.check_chapter_exercises(user, exerciserecord.exercise.chapter.id)


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
    kana_alt_blank = models.CharField(max_length=250, blank=True)
    kana_clean = models.CharField(max_length=250, blank=True)
    f_kana = models.CharField(max_length=250, blank=True)
    f_kanji = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if '(' in self.english:
            self.context = create_context(self.english)

        self.kana = hw_punctuation(self.kana)
        self.kanji = hw_punctuation(self.kanji)
        self.kana_all_blank, self.kana_alt_blank, self.kana_clean = create_blanks(self.kana, self.disamb_location, False)
        self.f_kana = create_splits(self.kana)
        self.f_kanji = create_splits(self.kanji)
        self.kana_all_blank = create_splits(self.kana_all_blank)
        self.kana_alt_blank = create_splits(self.kana_alt_blank)
        super(Sentence, self).save(*args, **kwargs)

    class Meta:
        ordering = ['lesson']


class SentenceRecordManager(models.Manager):
    """create and manage sentencerecords for each user"""

    def update_sentence_record(self, profile):
        usersentence = profile.currentlesson
        user = profile.user
        sentences = Sentence.objects.filter(lesson_id__exact=usersentence)

        if not SentenceRecord.objects.filter(user=user, sentence__lesson_id__exact=usersentence).exists() and len(sentences) > 0:
            for sen in sentences:
                self.create(user=user, sentence=sen)

    def initial_sentence_record(self, user):   # create the sentence records for lesson 1 when user is created
        sentences = Sentence.objects.filter(lesson_id__exact=1)

        if len(sentences) > 0:
            for sen in sentences:
                self.get_or_create(user=user, sentence=sen)


class SentenceRecord(models.Model):
    """tracking user progress for each sentence"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, blank=False, null=False)
    last_attempt = models.DateTimeField(default=timezone.now, blank=True)
    next_review = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)                          # number of consecutive corrects
    rating = models.IntegerField(default=0)                 # turns 1 if completed successfully in quiz
    objects = SentenceRecordManager()

    class Meta:
        ordering = ['next_review']


@receiver(user_logged_in)
def update_vr_sr_counts(sender, user, request, **kwargs):
    Profile.has_reviews(user)

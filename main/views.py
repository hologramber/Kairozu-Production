from itertools import zip_longest

import nltk
import re
import MeCab
from collections import Counter
from itertools import chain

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Profile, Expression, ExpressionRecord, Vocabulary, Lesson, Chapter, VocabRecord, SentenceRecord, Practice, Sentence, Exercise, ExerciseRecord, ExerciseSentence, GrammarNote


def collect_vocab_analysis(chapter_id):
    vocabularies = Vocabulary.objects.filter(chapter_id=chapter_id)
    vocabularies_all = Vocabulary.objects.filter(chapter__id__lte=chapter_id)
    allvocab = []
    for word in vocabularies:
        wordeng = re.sub(r'-san', '', word.english)
        wordeng = re.sub(r'to ', '', wordeng)
        wordeng = re.sub(r' \([^)]*\)', '', wordeng)
        wordeng = re.sub(r'/', ' ', wordeng)
        if " " in wordeng:
            wordswithspace = wordeng.split()
            for splitword in wordswithspace:
                allvocab.append(splitword)
        else:
            allvocab.append(wordeng)
    allvocab_all = []
    for word_all in vocabularies_all:
        wordeng_all = re.sub(r'-san', '', word_all.english)
        wordeng_all = re.sub(r'to ', '', wordeng_all)
        wordeng_all = re.sub(r' \([^)]*\)', '', wordeng_all)
        wordeng_all = re.sub(r'/', ' ', wordeng_all)
        if " " in wordeng_all:
            wordswithspace_all = wordeng_all.split()
            for splitword_all in wordswithspace_all:
                allvocab_all.append(splitword_all)
        else:
            allvocab_all.append(wordeng_all)
    return allvocab, allvocab_all


def remove_plurals(allwords_l):
    while 'the' in allwords_l: allwords_l.remove('the')
    while 'at' in allwords_l: allwords_l.remove('at')
    while 'will' in allwords_l: allwords_l.remove('will')
    while 'wont' in allwords_l: allwords_l.remove('wont')
    while 'is' in allwords_l: allwords_l.remove('is')
    while 'isnt' in allwords_l: allwords_l.remove('isnt')
    while 'are' in allwords_l: allwords_l.remove('are')
    while 'arent' in allwords_l: allwords_l.remove('arent')
    while 'an' in allwords_l: allwords_l.remove('an')
    while 'both' in allwords_l: allwords_l.remove('both')
    while 'neither' in allwords_l: allwords_l.remove('neither')
    while 'am' in allwords_l: allwords_l.remove('am')
    while 'nor' in allwords_l: allwords_l.remove('nor')
    while 'or' in allwords_l: allwords_l.remove('or')
    while 'not' in allwords_l: allwords_l.remove('not')
    while 'an' in allwords_l: allwords_l.remove('to')
    while 'and' in allwords_l: allwords_l.remove('and')
    while 'it' in allwords_l: allwords_l.remove('it')
    while 'shall' in allwords_l: allwords_l.remove('shall')

    allwords_s = []
    for plur in allwords_l:
        wordsing = re.sub(r'^cookies$', 'cookie', plur)
        wordsing = re.sub(r'^bananas$', 'banana', wordsing)
        wordsing = re.sub(r'^strawberries$', 'strawberry', wordsing)
        wordsing = re.sub(r'^books$', 'book', wordsing)
        wordsing = re.sub(r'^letters$', 'letter', wordsing)
        wordsing = re.sub(r'^bags$', 'bag', wordsing)
        wordsing = re.sub(r'^boxes$', 'box', wordsing)
        wordsing = re.sub(r'^employees$', 'employee', wordsing)
        wordsing = re.sub(r'^umbrellas$', 'umbrella', wordsing)
        wordsing = re.sub(r'^hats$', 'hat', wordsing)
        wordsing = re.sub(r'^pens$', 'pen', wordsing)
        wordsing = re.sub(r'^lawyers$', 'lawyer', wordsing)
        wordsing = re.sub(r'^bicycles$', 'bicycle', wordsing)
        wordsing = re.sub(r'^windows$', 'window', wordsing)
        wordsing = re.sub(r'^tickets$', 'ticket', wordsing)
        wordsing = re.sub(r'^magazines', 'magazine', wordsing)
        wordsing = re.sub(r'^dogs$', 'dog', wordsing)
        wordsing = re.sub(r'^movies$', 'movie', wordsing)
        wordsing = re.sub(r'^cats$', 'cat', wordsing)
        wordsing = re.sub(r'^newspapers$', 'newspaper', wordsing)
        wordsing = re.sub(r'^borrows$', 'borrow', wordsing)
        wordsing = re.sub(r'^buys$', 'buy', wordsing)
        wordsing = re.sub(r'^comes$', 'come', wordsing)
        wordsing = re.sub(r'^drinks$', 'drink', wordsing)
        wordsing = re.sub(r'^eats$', 'eat', wordsing)
        wordsing = re.sub(r'^goes$', 'go', wordsing)
        wordsing = re.sub(r'^opens$', 'open', wordsing)
        wordsing = re.sub(r'^listens$', 'listen', wordsing)
        wordsing = re.sub(r'^wakes$', 'wake', wordsing)
        wordsing = re.sub(r'^returns$', 'return', wordsing)
        wordsing = re.sub(r'^reads$', 'read', wordsing)
        wordsing = re.sub(r'^chairs$', 'chair', wordsing)
        wordsing = re.sub(r'^forks$', 'fork', wordsing)
        wordsing = re.sub(r'^notebooks$', 'notebook', wordsing)
        wordsing = re.sub(r'^spoons$', 'spoon', wordsing)
        wordsing = re.sub(r'^teachers$', 'teacher', wordsing)
        wordsing = re.sub(r'^vegetables$', 'vegetable', wordsing)
        wordsing = re.sub(r'^writes$', 'write', wordsing)
        wordsing = re.sub(r'^pencils$', 'pencil', wordsing)
        wordsing = re.sub(r'^students$', 'student', wordsing)
        wordsing = re.sub(r'^photos$', 'photo', wordsing)
        wordsing = re.sub(r'^teaches$', 'teach', wordsing)
        wordsing = re.sub(r'^pictures$', 'picture', wordsing)
        wordsing = re.sub(r'^knives$', 'knife', wordsing)
        wordsing = re.sub(r'^speaks$', 'speak', wordsing)
        wordsing = re.sub(r'^these$', 'this', wordsing)
        wordsing = re.sub(r'^those$', 'that', wordsing)
        wordsing = re.sub(r'^plays$', 'play', wordsing)
        wordsing = re.sub(r'^my$', 'i', wordsing)
        wordsing = re.sub(r'^mine$', 'i', wordsing)
        wordsing = re.sub(r'^hers$', 'she', wordsing)
        wordsing = re.sub(r'^her$', 'she', wordsing)
        wordsing = re.sub(r'^his$', 'he', wordsing)
        wordsing = re.sub(r'^yours$', 'you', wordsing)
        wordsing = re.sub(r'^your$', 'you', wordsing)
        wordsing = re.sub(r'^uses$', 'use', wordsing)
        wordsing = re.sub(r'^doors$', 'door', wordsing)
        wordsing = re.sub(r'^currently$', 'now', wordsing)
        wordsing = re.sub(r'^buses$', 'bus', wordsing)
        wordsing = re.sub(r'^cars$', 'car', wordsing)
        wordsing = re.sub(r'^flowers$', 'flower', wordsing)
        wordsing = re.sub(r'^americans$', 'american', wordsing)
        wordsing = re.sub(r'^apples$', 'apple', wordsing)
        wordsing = re.sub(r'^cars$', 'car', wordsing)
        wordsing = re.sub(r'^postcards$', 'postcard', wordsing)
        wordsing = re.sub(r'^museums$', 'museum', wordsing)
        wordsing = re.sub(r'^mountains$', 'mountain', wordsing)
        wordsing = re.sub(r'^futons$', 'futon', wordsing)
        wordsing = re.sub(r'^hates$', 'hateable', wordsing)
        wordsing = re.sub(r'^hate$', 'hateable', wordsing)
        wordsing = re.sub(r'^toilets$', 'toilet', wordsing)
        wordsing = re.sub(r'^watches$', 'watch', wordsing)
        wordsing = re.sub(r'^oclock$', 'time', wordsing)
        wordsing = re.sub(r'^likes$', 'likeable', wordsing)
        wordsing = re.sub(r'^like$', 'likeable', wordsing)
        wordsing = re.sub(r'^rivers$', 'river', wordsing)
        wordsing = re.sub(r'^trains$', 'train', wordsing)
        wordsing = re.sub(r'^restaurants$', 'restaurant', wordsing)
        wordsing = re.sub(r'^rooms$', 'room', wordsing)
        wordsing = re.sub(r'^theaters$', 'theater', wordsing)
        wordsing = re.sub(r'^kitchens$', 'kitchen', wordsing)
        wordsing = re.sub(r'^holidays$', 'holiday', wordsing)
        wordsing = re.sub(r'^nearby$', 'near', wordsing)
        wordsing = re.sub(r'^rent$', 'borrow', wordsing)
        wordsing = re.sub(r'^animals$', 'animal', wordsing)
        wordsing = re.sub(r'^computers$', 'computer', wordsing)
        wordsing = re.sub(r'^envelopes$', 'envelope', wordsing)
        wordsing = re.sub(r'^cards$', 'card', wordsing)
        wordsing = re.sub(r'^cafes$', 'cafe', wordsing)
        wordsing = re.sub(r'^dictionaries$', 'dictionary', wordsing)
        allwords_s.append(wordsing)
    return allwords_s


def analyze_sentences(sentences, allvocab, allvocab_all):
    mct = MeCab.Tagger("-Ochasen -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
    allwords = []
    for sentence in sentences:
        # ###################### JAPANESE ######################
        sentence.kprocess = re.sub(r'さん', '', sentence.kanji)
        sentence.kprocess = re.sub(r'　', '', sentence.kprocess)

        sentence.jpcab = []
        sentence.posids = []
        jparse = mct.parseToNode(sentence.kprocess)
        while jparse:
            if jparse.posid != 8 and jparse.posid != 0 and jparse.posid != 7:
                mct_split = jparse.feature.split(',')
                sentence.jpcab.append(mct_split[0])

                sentence.posids.append(jparse.posid)
            jparse = jparse.next

        # #################### ENGLISH ######################
        s_nopunct = re.sub(r'[.,?!]', "", sentence.english)
        s_nopunct = re.sub(r'\([^)]*\)', '', s_nopunct)
        s_nopunct = re.sub(r' a ', ' ', s_nopunct)

        s_token = nltk.word_tokenize(s_nopunct)
        s_taglist = [tag[1] for tag in nltk.pos_tag(s_token)]

        sentence.s_tags = [word[:-1] if len(word) > 2 else word for word in s_taglist]

        sentence.s_tokenize = re.sub(r'\'s', '', s_nopunct)
        sentence.s_tokenize = re.sub(r'-sans', '', sentence.s_tokenize)
        sentence.s_tokenize = re.sub(r'-san', '', sentence.s_tokenize)

        sentence.s_tokenize = nltk.word_tokenize(sentence.s_tokenize)
        allwords += sentence.s_tokenize

        allwords_l = [word.lower() for word in allwords]
        allvocab_l = [vocab.lower() for vocab in allvocab]
        allvocab_all_l = [vocab_all.lower() for vocab_all in allvocab_all]

        allwords_s = remove_plurals(allwords_l)

        sentence.fullcount = Counter(allwords_s).most_common()
        sentence.fullcount2 = '<br />'.join(map(str, sentence.fullcount))
        sentence.fullcount2 = re.sub(r'[\'()]', '', sentence.fullcount2)

        sentence.missingwords = list(set(allvocab_l) - set(allwords_s))
        sentence.missingwords = sorted(sentence.missingwords)

        sentence.missingvocab = list(set(allwords_s) - set(allvocab_all_l))
        sentence.missingvocab = sorted(sentence.missingvocab)
    return sentences


class SentenceAnalysisFullView(LoginRequiredMixin, ListView):
    template_name = 'main/sentenceanalysis_full.html'

    def get_context_data(self, **kwargs):
        context = super(SentenceAnalysisFullView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        sentences = Sentence.objects.filter(lesson__chapter__id__lte=chapter.id)
        allvocab, allvocab_all = collect_vocab_analysis(chapter.id)
        sentences = analyze_sentences(sentences, allvocab_all, allvocab_all)
        return sentences


class SentenceAnalysisChapterView(LoginRequiredMixin, ListView):
    template_name = 'main/sentenceanalysis.html'

    def get_context_data(self, **kwargs):
        context = super(SentenceAnalysisChapterView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['last'] = chapter.id-1
        context['next'] = chapter.id+1
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter_now = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        sentences = Sentence.objects.filter(lesson__chapter__id__exact=chapter_now.id)
        allvocab, allvocab_all = collect_vocab_analysis(chapter_now.id)
        sentences = analyze_sentences(sentences, allvocab, allvocab_all)
        return sentences


class SentenceAnalysisView(LoginRequiredMixin, ListView):
    template_name = 'main/sentenceanalysis.html'

    def get_context_data(self, **kwargs):
        context = super(SentenceAnalysisView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['last'] = lesson.id-1
        context['next'] = lesson.id+1
        context['chapter'] = lesson.chapter
        context['lesson'] = lesson
        return context

    def get_queryset(self):
        lesson_now = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        sentences = Sentence.objects.filter(lesson=lesson_now)
        allvocab, allvocab_all = collect_vocab_analysis(lesson_now.chapter.id)
        sentences = analyze_sentences(sentences, allvocab, allvocab_all)
        return sentences


def analyze_practices(practices, allvocab, allvocab_all):
    mct = MeCab.Tagger("-Ochasen -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
    allwords = []
    for practice in practices:
        # ###################### JAPANESE ######################
        pone_kprocess = re.sub(r'さん', '', practice.pone_kanji)
        ptwo_kprocess = re.sub(r'さん', '', practice.ptwo_kanji)
        practice.pone_kprocess = re.sub(r'　', '', pone_kprocess)
        practice.ptwo_kprocess = re.sub(r'　', '', ptwo_kprocess)

        practice.pone_jpcab = []
        practice.pone_posids = []
        pone_jparse = mct.parseToNode(practice.pone_kprocess)
        while pone_jparse:
            if pone_jparse.posid != 8 and pone_jparse.posid != 0 and pone_jparse.posid != 7:
                mct_split = pone_jparse.feature.split(',')
                practice.pone_jpcab.append(mct_split[0])
                practice.pone_posids.append(pone_jparse.posid)
            pone_jparse = pone_jparse.next

        practice.ptwo_jpcab = []
        practice.ptwo_posids = []
        ptwo_jparse = mct.parseToNode(practice.ptwo_kprocess)
        while ptwo_jparse:
            if ptwo_jparse.posid != 8 and ptwo_jparse.posid != 0 and ptwo_jparse.posid != 7:
                mct_split = ptwo_jparse.feature.split(',')
                practice.ptwo_jpcab.append(mct_split[0])
                practice.ptwo_posids.append(ptwo_jparse.posid)
            ptwo_jparse = ptwo_jparse.next

        practice.poscompare = ''
        for x, y in zip_longest(reversed(practice.pone_posids), reversed(practice.ptwo_posids)):
            if x == y:
                practice.poscompare = '<span class="gre_c smaller caps">o</span>' + practice.poscompare
            elif x is None or y is None:
                practice.poscompare = '<span class="gra_c smaller caps">-</span>' + practice.poscompare
            else:
                practice.poscompare = '<span class="red_c smaller caps">x</span>' + practice.poscompare

        practice.poscomparelr = ''
        for x, y in zip_longest(practice.pone_posids, practice.ptwo_posids):
            if x == y:
                practice.poscomparelr += '<span class="gre_c smaller caps">o</span>'
            elif x is None or y is None:
                practice.poscomparelr += '<span class="gra_c smaller caps">-</span>'
            else:
                practice.poscomparelr += '<span class="red_c smaller caps">x</span>'

        practice.poscomparetype = ''
        for x, y in zip_longest(reversed(practice.pone_jpcab), reversed(practice.ptwo_jpcab)):
            if x == y:
                practice.poscomparetype = '<span class="gre_c smaller caps">o</span>' + practice.poscomparetype
            elif x is None or y is None:
                practice.poscomparetype = '<span class="gra_c smaller caps">-</span>' + practice.poscomparetype
            else:
                practice.poscomparetype = '<span class="red_c smaller caps">x</span>' + practice.poscomparetype

        practice.poscomparetypelr = ''
        for x, y in zip_longest(practice.pone_jpcab, practice.ptwo_jpcab):
            if x == y:
                practice.poscomparetypelr += '<span class="gre_c smaller caps">o</span>'
            elif x is None or y is None:
                practice.poscomparetypelr += '<span class="gra_c smaller caps">-</span>'
            else:
                practice.poscomparetypelr += '<span class="red_c smaller caps">x</span>'

        # ###################### ENGLISH ######################
        pone_nopunct = re.sub(r'[.,?!]', "", practice.pone_english)
        ptwo_nopunct = re.sub(r'[.,?!]', "", practice.ptwo_english)

        pone_nopunct = re.sub(r'\([^)]*\)', '', pone_nopunct)
        ptwo_nopunct = re.sub(r'\([^)]*\)', '', ptwo_nopunct)

        pone_nopunct = re.sub(r' a ', ' ', pone_nopunct)
        ptwo_nopunct = re.sub(r' a ', ' ', ptwo_nopunct)

        pone_token = nltk.word_tokenize(pone_nopunct)
        ptwo_token = nltk.word_tokenize(ptwo_nopunct)
        pone_taglist = [tag[1] for tag in nltk.pos_tag(pone_token)]
        ptwo_taglist = [tag[1] for tag in nltk.pos_tag(ptwo_token)]

        practice.pone_tags = [word[:-1] if len(word) > 2 else word for word in pone_taglist]
        practice.ptwo_tags = [word[:-1] if len(word) > 2 else word for word in ptwo_taglist]

        practice.enposcompare = ''
        for x, y in zip_longest(reversed(practice.pone_tags), reversed(practice.ptwo_tags)):
            if x == y:
                practice.enposcompare = '<span class="gre_c smaller caps">o</span>' + practice.enposcompare
            elif x is None or y is None:
                practice.enposcompare = '<span class="gra_c smaller caps">-</span>' + practice.enposcompare
            else:
                practice.enposcompare = '<span class="red_c smaller caps">x</span>' + practice.enposcompare

        practice.enposcomparelr = ''
        for x, y in zip_longest(practice.pone_tags, practice.ptwo_tags):
            if x == y:
                practice.enposcomparelr += '<span class="gre_c smaller caps">o</span>'
            elif x is None or y is None:
                practice.enposcomparelr += '<span class="gra_c smaller caps">-</span>'
            else:
                practice.enposcomparelr += '<span class="red_c smaller caps">x</span>'

        practice.pone_tokenize = re.sub(r'\'s', '', pone_nopunct)
        practice.ptwo_tokenize = re.sub(r'\'s', '', ptwo_nopunct)

        practice.pone_tokenize = re.sub(r'\'', '', practice.pone_tokenize)
        practice.ptwo_tokenize = re.sub(r'\'', '', practice.ptwo_tokenize)

        practice.pone_tokenize = re.sub(r'-sans', '', practice.pone_tokenize)
        practice.pone_tokenize = re.sub(r'-san', '', practice.pone_tokenize)

        practice.ptwo_tokenize = re.sub(r'-sans', '', practice.ptwo_tokenize)
        practice.ptwo_tokenize = re.sub(r'-san', '', practice.ptwo_tokenize)

        practice.pone_tokenize = nltk.word_tokenize(practice.pone_tokenize)
        allwords += practice.pone_tokenize
        practice.ptwo_tokenize = nltk.word_tokenize(practice.ptwo_tokenize)
        allwords += practice.ptwo_tokenize

        allwords_l = [x.lower() for x in allwords if not (x[0].isdigit())]
        allvocab_l = [x.lower() for x in allvocab if not (x[0].isdigit())]
        allvocab_all_l = [x.lower() for x in allvocab_all if not (x[0].isdigit())]

        allwords_s = remove_plurals(allwords_l)

        practice.fullcount = Counter(allwords_s).most_common()
        practice.fullcount2 = '<br />'.join(map(str, practice.fullcount))
        practice.fullcount2 = re.sub(r'[\'()]', '', practice.fullcount2)

        practice.missingwords = list(set(allvocab_l) - set(allwords_s))
        practice.missingwords = sorted(practice.missingwords)

        practice.missingvocab = list(set(allwords_s) - set(allvocab_all_l))
        practice.missingvocab = sorted(practice.missingvocab)
    return practices


class PracticeAnalysisFullView(LoginRequiredMixin, ListView):
    template_name = 'main/practiceanalysis_full.html'

    def get_context_data(self, **kwargs):
        context = super(PracticeAnalysisFullView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        practices = Practice.objects.filter(lesson__chapter__id__lte=chapter.id)
        allvocab, allvocab_all = collect_vocab_analysis(chapter.id)
        practices = analyze_practices(practices, allvocab_all, allvocab_all)
        return practices


class PracticeAnalysisChapterView(LoginRequiredMixin, ListView):
    template_name = 'main/practiceanalysis.html'

    def get_context_data(self, **kwargs):
        context = super(PracticeAnalysisChapterView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['last'] = chapter.id-1
        context['next'] = chapter.id+1
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter_now = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        practices = Practice.objects.filter(lesson__chapter__id__exact=chapter_now.id)
        allvocab, allvocab_all = collect_vocab_analysis(chapter_now.id)
        practices = analyze_practices(practices, allvocab, allvocab_all)
        return practices


class PracticeAnalysisView(LoginRequiredMixin, ListView):
    template_name = 'main/practiceanalysis.html'

    def get_context_data(self, **kwargs):
        context = super(PracticeAnalysisView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['last'] = lesson.id-1
        context['next'] = lesson.id+1
        context['chapter'] = lesson.chapter
        context['lesson'] = lesson
        return context

    def get_queryset(self):
        lesson_now = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        practices = Practice.objects.filter(lesson=lesson_now)
        allvocab, allvocab_all = collect_vocab_analysis(lesson_now.chapter.id)
        practices = analyze_practices(practices, allvocab, allvocab_all)
        return practices


class AjaxTemplateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)


# class NewIssueView(LoginRequiredMixin, AjaxTemplateMixin, CreateView):
#     template_name = 'main/siteissue_form.html'
#     model = SiteIssue
#     fields = ['report_type', 'report_comment']
#
#     def form_valid(self, form):
#         if SiteIssue.objects.filter(report_by_user=self.request.user.id).count() >= 15:
#             messages.add_message(self.request, messages.ERROR, 'Sorry! For the sake of my database, only 15 bug reports per day/user. Email kairozu@kairozu.com for help.')
#         else:
#             form.instance.report_by_user = self.request.user.id
#             form.instance.report_from_url = self.request.META.get("HTTP_REFERER")
#             form.save()
#             messages.add_message(self.request, messages.SUCCESS, 'Bug submitted! Apologies for the trouble, but thank you for letting us know.')
#         if self.request.is_ajax():
#             return render(self.request, 'main/siteissue_done.html')
#         else:
#             return render(self.request, 'index.html')


# where users enter chapters; grid of red sun chapters/progress
class MainView(LoginRequiredMixin, ListView):
    model = Chapter
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        # messages.add_message(self.request, messages.SUCCESS, 'Bug submitted! Apologies for the trouble, but thank you for letting us know.')
        return context


# front interface for each chapter (prior to entering vocab/grammar/etc)
class ChapterInterfaceView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/interface.html'

    def get_context_data(self, **kwargs):
        context = super(ChapterInterfaceView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentchapter:
            return True



# list of vocabulary per chapter
class VocabListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/vocablist.html'

    def get_context_data(self, **kwargs):
        context = super(VocabListView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter_now = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        return Vocabulary.objects.filter(chapter=chapter_now)

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentvocab:
            return True


# vocabulary quiz first-load (future loads aren't full refreshes)
class VocabQuizView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/vocabquiz.html'

    def get_context_data(self, **kwargs):
        context = super(VocabQuizView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentvocab:
            return True


def vocab_check(request, chapter_id):
    vocab_code = request.POST['vocab_code']
    vocabrecord_id = int(request.POST['vocabrecord_id'])
    if vocab_code == 'C':
        VocabRecord.correct_attempt(vocabrecord_id)
    elif vocab_code == 'N':
        VocabRecord.new_attempt(vocabrecord_id)
    elif vocab_code == 'I':
        VocabRecord.incorrect_attempt(vocabrecord_id)
    return HttpResponseRedirect(reverse('main:vocabgrab', kwargs={'chapter_id': chapter_id}))


class VocabSuccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/success.html'

    def get_context_data(self, **kwargs):
        context = super(VocabSuccessView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        context['which_success'] = chapter.title + " Vocabulary Quiz."
        currentc = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentc'] = currentc
        context['exercisec'] = Exercise.objects.get(exercise_order__exact=self.request.user.profile.currentexercise)
        context['chapter_all'] = Chapter.objects.all()
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentvocab:
            return True


# list of expressions per chapter
class ExpressionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/expressionlist.html'

    def get_context_data(self, **kwargs):
        context = super(ExpressionListView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter_now = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        return Expression.objects.filter(chapter=chapter_now)

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentexpression:
            return True


# expression quiz first-load (future loads aren't full refreshes)
class ExpressionQuizView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/expressionquiz.html'

    def get_context_data(self, **kwargs):
        context = super(ExpressionQuizView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentexpression:
            return True


def expression_check(request, chapter_id):
    expression_code = request.POST['expression_code']
    expressionrecord_id = int(request.POST['expressionrecord_id'])
    if expression_code == 'C':
        ExpressionRecord.correct_attempt(expressionrecord_id)
    elif expression_code == 'N':
        ExpressionRecord.new_attempt(expressionrecord_id)
    elif expression_code == 'I':
        ExpressionRecord.incorrect_attempt(expressionrecord_id)
    return HttpResponseRedirect(reverse('main:expressiongrab', kwargs={'chapter_id': chapter_id}))


class ExpressionSuccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/success.html'

    def get_context_data(self, **kwargs):
        context = super(ExpressionSuccessView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        context['which_success'] = chapter.title + " Expression Quiz."
        currentc = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentc'] = currentc
        context['exercisec'] = Exercise.objects.get(exercise_order__exact=self.request.user.profile.currentexercise)
        context['chapter_all'] = Chapter.objects.all()
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentexpression:
            return True


# interface for each grammar point (title + grammar + point + examples + more info)
class LessonView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/lesson.html'

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['lesson'] = lesson
        context['chapter'] = lesson.chapter
        context['pieces'] = lesson.lesson_pieces()
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['lesson_id']) <= self.request.user.profile.currentlesson:
            return True


class GrammarNoteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/grammarnote.html'

    def get_context_data(self, **kwargs):
        context = super(GrammarNoteView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        if GrammarNote.objects.filter(lesson__id__exact=self.kwargs['lesson_id']).exists():
            grammarnote = GrammarNote.objects.get(lesson__id__exact=self.kwargs['lesson_id'])
            context['grammarnote'] = grammarnote
        context['lesson'] = lesson
        context['chapter'] = lesson.chapter
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['lesson_id']) <= self.request.user.profile.currentlesson:
            return True


# practice quiz first-load (future loads aren't full refreshes)
class PracticeQuizView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.profile.strictmode:
            return ['main/practicequiz_strict.html']
        else:
            return ['main/practicequiz.html']

    def get_context_data(self, **kwargs):
        context = super(PracticeQuizView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['chapter'] = lesson.chapter
        context['lesson'] = lesson
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['lesson_id']) <= self.request.user.profile.currentpractice:
            return True


def practice_check(request, lesson_id):
    pindex = int(request.POST['pindex'])
    return HttpResponseRedirect(reverse('main:practicegrab', kwargs={'lesson_id': lesson_id, 'pindex': pindex}))


def practice_reset(request, lesson_id):
    reseturl = reverse('main:practicequiz', kwargs={'lesson_id': lesson_id})
    return HttpResponseRedirect(reseturl)


class PracticeSuccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/success.html'

    def get_context_data(self, **kwargs):
        context = super(PracticeSuccessView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['lesson'] = lesson
        context['which_success'] = "Practice Quiz for \"" + lesson.title + "\""
        context['chapter'] = lesson.chapter
        currentc = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentc'] = currentc
        currentl = get_object_or_404(Lesson, pk=self.request.user.profile.currentlesson)
        context['currentl'] = currentl
        context['exercisec'] = Exercise.objects.get(exercise_order__exact=self.request.user.profile.currentexercise)
        context['chapter_all'] = Chapter.objects.all()
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['lesson_id']) <= self.request.user.profile.currentpractice:
            return True


# sentence quiz first-load (future loads aren't full refreshes)
class SentenceQuizView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.profile.strictmode:
            return ['main/sentencequiz_strict.html']
        else:
            return ['main/sentencequiz.html']

    def get_context_data(self, **kwargs):
        context = super(SentenceQuizView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['chapter'] = lesson.chapter
        context['lesson'] = lesson
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['lesson_id']) <= self.request.user.profile.currentpractice:
            return True


def sentence_check(request, lesson_id):
    sentence_code = request.POST['sentence_code']
    sentencerecord_id = int(request.POST['sentencerecord_id'])
    if sentence_code == 'C':
        SentenceRecord.correct_attempt(sentencerecord_id)
    elif sentence_code == 'N':
        SentenceRecord.new_attempt(sentencerecord_id)
    elif sentence_code == 'I':
        SentenceRecord.incorrect_attempt(sentencerecord_id)
    return HttpResponseRedirect(reverse('main:sentencegrab', kwargs={'lesson_id': lesson_id}))


class SentenceSuccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/success.html'

    def get_context_data(self, **kwargs):
        context = super(SentenceSuccessView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['which_success'] = "Sentence Quiz for \"" + lesson.title + "\""
        context['chapter'] = lesson.chapter
        currentc = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentc'] = currentc
        currentl = get_object_or_404(Lesson, pk=self.request.user.profile.currentlesson)
        context['currentl'] = currentl
        context['exercisec'] = Exercise.objects.get(exercise_order__exact=self.request.user.profile.currentexercise)
        context['chapter_all'] = Chapter.objects.all()
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['lesson_id']) <= self.request.user.profile.currentlesson:
            return True


class SummaryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/summary.html'

    def get_context_data(self, **kwargs):
        context = super(SummaryView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter_now = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        return Lesson.objects.filter(chapter=chapter_now)

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentchapter:
            return True


# vocabulary quiz first-load (future loads aren't full refreshes)
class ReviewVocabView(LoginRequiredMixin, TemplateView):
    template_name = 'main/vocabreview.html'


def reviewvocab_check(request):
    vocab_code = request.POST['vocab_code']
    vocabrecord_id = int(request.POST['vocabrecord_id'])
    if vocab_code == 'C':
        VocabRecord.review_correct_attempt(vocabrecord_id)
    elif vocab_code == 'N':
        VocabRecord.review_new_attempt(vocabrecord_id)
    elif vocab_code == 'I':
        VocabRecord.review_incorrect_attempt(vocabrecord_id)
    return HttpResponseRedirect(reverse('main:reviewvocabgrab'))


class ReviewVocabCurrentView(LoginRequiredMixin, ListView):
    template_name = 'main/vocabcurrent.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewVocabCurrentView, self).get_context_data(**kwargs)
        currentchapter = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentchapter'] = currentchapter
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        return VocabRecord.objects.filter(user_id=self.request.user.id).order_by('-next_review')[:10]


class ReviewSentenceView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.profile.strictmode:
            return ['main/sentencereview_strict.html']
        else:
            return ['main/sentencereview.html']


def reviewsentence_check(request):
    sentence_code = request.POST['sentence_code']
    sentencerecord_id = int(request.POST['sentencerecord_id'])

    if sentence_code == 'C':
        SentenceRecord.review_correct_attempt(sentencerecord_id)
    elif sentence_code == 'N':
        SentenceRecord.review_new_attempt(sentencerecord_id)
    elif sentence_code == 'I':
        SentenceRecord.review_incorrect_attempt(sentencerecord_id)
    return HttpResponseRedirect(reverse('main:reviewsentencegrab'))


class ReviewSentenceCurrentView(LoginRequiredMixin, ListView):
    template_name = 'main/sentencecurrent.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewSentenceCurrentView, self).get_context_data(**kwargs)
        currentchapter = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentchapter'] = currentchapter
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        return SentenceRecord.objects.filter(user_id=self.request.user.id).order_by('-next_review')[:10]


class ReviewExpressionView(LoginRequiredMixin, TemplateView):
    template_name = 'main/expressionreview.html'


def reviewexpression_check(request):
    expression_code = request.POST['expression_code']
    expressionrecord_id = int(request.POST['expressionrecord_id'])

    if expression_code == 'C':
        ExpressionRecord.review_correct_attempt(expressionrecord_id)
    elif expression_code == 'N':
        ExpressionRecord.review_new_attempt(expressionrecord_id)
    elif expression_code == 'I':
        ExpressionRecord.review_incorrect_attempt(expressionrecord_id)
    return HttpResponseRedirect(reverse('main:reviewexpressiongrab'))


class ReviewExpressionCurrentView(LoginRequiredMixin, ListView):
    template_name = 'main/expressioncurrent.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewExpressionCurrentView, self).get_context_data(**kwargs)
        currentchapter = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentchapter'] = currentchapter
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        return ExpressionRecord.objects.filter(user_id=self.request.user.id).order_by('-next_review')[:10]


class ExercisesAdminView(LoginRequiredMixin, TemplateView):
    template_name = 'main/admin_exercises.html'

    def get_context_data(self, **kwargs):
        context = super(ExercisesAdminView, self).get_context_data(**kwargs)
        prompts = Exercise.exercise_pieces_admin_prompt(self.kwargs['chapter_id'])
        context['prompts'] = prompts
        context['sentences'] = Exercise.exercise_pieces_admin_sentence(self.kwargs['chapter_id'])
        return context


class ExercisesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/exercises.html'

    def get_context_data(self, **kwargs):
        context = super(ExercisesView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter_now = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        return Exercise.objects.filter(chapter=chapter_now).order_by('exercise_order')

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentstory:
            return True


class ExercisePassageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/passage.html'

    def get_context_data(self, **kwargs):
        context = super(ExercisePassageView, self).get_context_data(**kwargs)
        exercise = get_object_or_404(Exercise, pk=self.kwargs['exercise_id'])
        context['exercise'] = exercise
        context['chapter'] = exercise.chapter
        return context

    def get_queryset(self):
        exercise_id = get_object_or_404(Exercise, pk=self.kwargs['exercise_id'])
        return ExerciseSentence.objects.filter(exercise_id=exercise_id)

    def test_func(self, **kwargs):
        if int(self.kwargs['exercise_id']) <= self.request.user.profile.currentexercise:
            return True


def exercise_passage_check(request, chapter_id, exercise_id):
    passage_index = int(request.POST['passage_index'])
    return HttpResponseRedirect(reverse('main:exercisepassagegrab', kwargs={'chapter_id': chapter_id, 'exercise_id': exercise_id, 'passage_index': passage_index}))


def exercise_passage_grade(request, chapter_id, exercise_id):
    exerciserecord_user = ExerciseRecord.objects.get(user_id=request.user.id, exercise__id__exact=exercise_id)
    passage_grade = request.POST['passage_grade']
    ExerciseRecord.update_grade(exerciserecord_user.id, passage_grade, request.user)
    return HttpResponseRedirect(reverse('main:exercisepassagesuccess', kwargs={'chapter_id': chapter_id, 'exercise_id': exercise_id}))


class ExercisePassageSuccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/passagesuccess.html'

    def get_context_data(self, **kwargs):
        context = super(ExercisePassageSuccessView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        currentc = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        erecord = ExerciseRecord.objects.get(user_id=self.request.user.id, exercise__id__exact=self.kwargs['exercise_id'])
        erecord.newscore = round(erecord.score*100,1)
        context['chapter'] = chapter
        context['currentc'] = currentc
        context['exercisec'] = Exercise.objects.get(exercise_order__exact=self.request.user.profile.currentexercise)
        context['chapter_all'] = Chapter.objects.all()
        context['erecord'] = erecord
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['exercise_id']) <= self.request.user.profile.currentexercise:
            return True


class ExerciseDialogueView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/dialogue.html'

    def get_context_data(self, **kwargs):
        context = super(ExerciseDialogueView, self).get_context_data(**kwargs)
        exercise = get_object_or_404(Exercise, pk=self.kwargs['exercise_id'])
        context['exercise'] = exercise
        context['chapter'] = exercise.chapter
        context['pieces'] = exercise.exercise_pieces()
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['exercise_id']) <= self.request.user.profile.currentexercise:
            return True


def exercise_dialogue_check(request, chapter_id, exercise_id):
    dialogue_index = int(request.POST['dialogue_index'])
    return HttpResponseRedirect(reverse('main:exercisedialoguegrab', kwargs={'chapter_id': chapter_id, 'exercise_id': exercise_id, 'dialogue_index': dialogue_index}))


def exercise_dialogue_grade(request, chapter_id, exercise_id):
    exerciserecord_user = ExerciseRecord.objects.get(user_id=request.user.id, exercise__id__exact=exercise_id)
    dialogue_grade = request.POST['dialogue_grade']
    ExerciseRecord.update_grade(exerciserecord_user.id, dialogue_grade, request.user)
    return HttpResponseRedirect(reverse('main:exercisedialoguesuccess', kwargs={'chapter_id': chapter_id, 'exercise_id': exercise_id}))


class ExerciseDialogueSuccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/dialoguesuccess.html'

    def get_context_data(self, **kwargs):
        context = super(ExerciseDialogueSuccessView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        currentc = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        erecord = ExerciseRecord.objects.get(user_id=self.request.user.id, exercise__id__exact=self.kwargs['exercise_id'])
        erecord.newscore = round(erecord.score*100,1)
        context['chapter'] = chapter
        context['currentc'] = currentc
        context['exercisec'] = Exercise.objects.get(exercise_order__exact=self.request.user.profile.currentexercise)
        context['chapter_all'] = Chapter.objects.all()
        context['erecord'] = erecord
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['exercise_id']) <= self.request.user.profile.currentexercise:
            return True


class ProgressView(LoginRequiredMixin, ListView):
    template_name = 'main/progress.html'

    def get_context_data(self, **kwargs):
        context = super(ProgressView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        context['vmastery'] = Profile.chapter_mastery_level(self.request.user)
        return context

    def get_queryset(self):
        vocabs = VocabRecord.objects.filter(user_id=self.request.user.id, rating__gt=0, score__lte=2).order_by('-score')
        expressions = ExpressionRecord.objects.filter(user_id=self.request.user.id, rating__gt=0, score__lte=2).order_by('-score')
        sentences = SentenceRecord.objects.filter(user_id=self.request.user.id, rating__gt=0, score__lte=2).order_by('-score')
        result_list = sorted(chain(vocabs, expressions, sentences), key=lambda instance: instance.score)
        return result_list
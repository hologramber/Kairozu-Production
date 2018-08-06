from itertools import chain
import json
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile, Expression, ExpressionRecord, Vocabulary, Practice, Lesson, Chapter, VocabRecord, SentenceRecord, Exercise, ExerciseRecord, ExerciseSentence, ExercisePrompt, GrammarNote, Flashcard
from .forms import ValidateFinishForm, ValidateExerciseFinish, FlashcardForm
from .serializers import VocabRecordSerializer, ExpressionRecordSerializer, SentenceRecordSerializer, FlashcardSerializer

error_finish = 'There was a problem with saving your current progress. Please e-mail kairozu@kairozu.com if you suspect this is an error.'
error_data = {'error': True}
loop_data = {'loop': True}
save_data = {'save': True}

# where users enter chapters; grid of red sun chapters/progress
class MainView(LoginRequiredMixin, ListView):
    model = Chapter
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        # messages.add_message(self.request, messages.SUCCESS, '...')
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


class ProgressView(LoginRequiredMixin, ListView):
    template_name = 'main/progress.html'

    def get_context_data(self, **kwargs):
        context = super(ProgressView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        context['vmastery'] = Profile.chapter_mastery_level(self.request.user)
        return context

    def get_queryset(self):
        vocabs = VocabRecord.objects.filter(user_id=self.request.user.id, rating__gt=0, score__lte=2)[:40]
        expressions = ExpressionRecord.objects.filter(user_id=self.request.user.id, rating__gt=0, score__lte=2)[:20]
        sentences = SentenceRecord.objects.filter(user_id=self.request.user.id, rating__gt=0, score__lte=2)[:40]
        result_list = sorted(chain(vocabs, expressions, sentences), key=lambda instance: instance.next_review)
        return result_list


def last_query(request, query_type, query_id):
    if query_type == 'VQ':
        lq = VocabRecord.objects.filter(user_id=request.user.id, vocab__chapter_id__exact=query_id).order_by('last_attempt').first()


# #################################################################################
# ################################## VOCABULARY ###################################
# #################################################################################

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
    template_name = 'main/vocabq.html'

    def get_context_data(self, **kwargs):
        context = super(VocabQuizView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentvocab:
            return True


@require_http_methods(["POST"])
def vocabsave(request, chapter_id):
    vr_queryset = VocabRecord.objects.filter(user_id=request.user.id, vocab__chapter_id__exact=chapter_id)
    vrupdate = VocabRecordSerializer(vr_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
    if vrupdate.is_valid():
        vrupdate.save()
        return JsonResponse(save_data)
    else:
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)


@require_http_methods(["POST"])
def vocabfinish(request, chapter_id):
    if request.user.profile.currentvocab < int(chapter_id):
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)
    else:
        vr_queryset = VocabRecord.objects.filter(user_id=request.user.id, vocab__chapter_id__exact=chapter_id)
        vrupdate = VocabRecordSerializer(vr_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
        if vrupdate.is_valid():
            vrupdate.save()
            if int(chapter_id) < request.user.profile.currentvocab:
                return JsonResponse(loop_data)
            elif int(chapter_id) == request.user.profile.currentvocab:
                vrecords = VocabRecord.objects.filter(user_id=request.user.id, vocab__chapter__id__exact=chapter_id, rating__lte=0)
                if vrecords is None:
                    Profile.graduate_vocab(request.user, chapter_id)
                    return HttpResponseRedirect(reverse('main:vocabsuccess', kwargs={'chapter_id': chapter_id}))
                else:
                    return JsonResponse(loop_data)
        else:
            return JsonResponse(error_data)


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


# #################################################################################
# ############################## END VOCABULARY ###################################
# #################################################################################

# #################################################################################
# ############################## EXPRESSIONS ######################################
# #################################################################################

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
    template_name = 'main/expressionq.html'

    def get_context_data(self, **kwargs):
        context = super(ExpressionQuizView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentexpression:
            return True


@require_http_methods(["POST"])
def expressionsave(request, chapter_id):
    er_queryset = ExpressionRecord.objects.filter(user_id=request.user.id, express__chapter_id__exact=chapter_id)
    erupdate = ExpressionRecordSerializer(er_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
    if erupdate.is_valid():
        erupdate.save()
        return JsonResponse(save_data)
    else:
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)


@require_http_methods(["POST"])
def expressionfinish(request, chapter_id):
    if request.user.profile.currentexpression < int(chapter_id):
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)
    else:
        er_queryset = ExpressionRecord.objects.filter(user_id=request.user.id, express__chapter_id__exact=chapter_id)
        erupdate = ExpressionRecordSerializer(er_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
        if erupdate.is_valid():
            erupdate.save()
            if int(chapter_id) < request.user.profile.currentexpression:
                return JsonResponse(loop_data)
            elif int(chapter_id) == request.user.profile.currentexpression:
                erecords = ExpressionRecord.objects.filter(user_id=request.user.id, express__chapter_id__exact=chapter_id, rating__lte=0)
                if erecords is None:
                    Profile.graduate_expression(request.user, chapter_id)
                    return HttpResponseRedirect(reverse('main:expressionsuccess', kwargs={'chapter_id': chapter_id}))
                else:
                    return JsonResponse(loop_data)
        else:
            return JsonResponse(error_data)


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

# #################################################################################
# ############################# END EXPRESSIONS ###################################
# #################################################################################

# #################################################################################
# ############################# PRACTICES #########################################
# #################################################################################

# practice quiz first-load (future loads aren't full refreshes)
class PracticeQuizView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/practiceq.html'

    def get_context_data(self, **kwargs):
        context = super(PracticeQuizView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['chapter'] = lesson.chapter
        context['lesson'] = lesson
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['lesson_id']) <= self.request.user.profile.currentpractice:
            return True

@require_http_methods(["POST"])
def practicefinish(request, lesson_id):
    if request.user.profile.currentpractice < int(lesson_id):
        return JsonResponse(error_data)
    else:
        form = ValidateFinishForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['q']
            totalq = form.cleaned_data['totalq']
            if q == totalq == Practice.objects.filter(lesson_id__exact=lesson_id).count():
                if request.user.profile.currentpractice == int(lesson_id):
                    Profile.graduate_practice(request.user, lesson_id)
                return HttpResponseRedirect(reverse('main:practicesuccess', kwargs={'lesson_id': lesson_id}))
            else:   # if # of questions doesn't line up
                messages.add_message(request, messages.ERROR, error_finish)
                return JsonResponse(error_data)
        else:   # if form is not valid
            messages.add_message(request, messages.ERROR, error_finish)
            return JsonResponse(error_data)


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

# #################################################################################
# ############################### END PRACTICES ###################################
# #################################################################################

# #################################################################################
# ############################### SENTENCES #######################################
# #################################################################################

# sentence quiz first-load (future loads aren't full refreshes)
class SentenceQuizView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/sentenceq.html'

    def get_context_data(self, **kwargs):
        context = super(SentenceQuizView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['chapter'] = lesson.chapter
        context['lesson'] = lesson
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['lesson_id']) <= self.request.user.profile.currentpractice:
            return True


@require_http_methods(["POST"])
def sentencesave(request, lesson_id):
    sr_queryset = SentenceRecord.objects.filter(user_id=request.user.id, sentence__lesson__id__exact=lesson_id)
    srupdate = SentenceRecordSerializer(sr_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
    if srupdate.is_valid():
        srupdate.save()
        return JsonResponse(save_data)
    else:
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)


@require_http_methods(["POST"])
def sentencefinish(request, lesson_id):
    if request.user.profile.currentlesson < int(lesson_id):
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)
    else:
        sr_queryset = SentenceRecord.objects.filter(user_id=request.user.id, sentence__lesson__id__exact=lesson_id)
        srupdate = SentenceRecordSerializer(sr_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
        if srupdate.is_valid():
            srupdate.save()
            if int(lesson_id) < request.user.profile.currentlesson:
                return JsonResponse(loop_data)
            elif int(lesson_id) == request.user.profile.currentlesson:
                srecords = SentenceRecord.objects.filter(user_id=request.user.id, sentence__lesson__id__exact=lesson_id, rating__lte=0)
                if srecords is None:
                    Profile.graduate_lesson(request.user, lesson_id)
                    return HttpResponseRedirect(reverse('main:sentencesuccess', kwargs={'lesson_id': lesson_id}))
                else:
                    return JsonResponse(loop_data)
        else:
            return JsonResponse(error_data)


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

# #################################################################################
# ################################ END SENTENCES ##################################
# #################################################################################

# #################################################################################
# ################################ REVIEWS ########################################
# #################################################################################

# vocabulary quiz first-load (future loads aren't full refreshes)
class ReviewVocabView(LoginRequiredMixin, TemplateView):
    template_name = 'main/vocabq_review.html'


@require_http_methods(["POST"])
def reviewvocabsave(request):
    vr_queryset = VocabRecord.objects.filter(user_id=request.user.id, next_review__lte=datetime.now())
    vrupdate = VocabRecordSerializer(vr_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
    if vrupdate.is_valid():
        vrupdate.save()
        return JsonResponse(save_data)
    else:
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)


# @require_http_methods(["POST"])
# def reviewvocabfinish(request):
#     vr_queryset = VocabRecord.objects.filter(user_id=request.user.id, next_review__lte=datetime.now())
#     vrupdate = VocabRecordSerializer(vr_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
#     if vrupdate.is_valid():
#         vrupdate.save()
#         vrecords = VocabRecord.objects.filter(user_id=request.user.id, next_review__lte=datetime.now())[:10]
#         if vrecords is None:
#             return HttpResponseRedirect(reverse('main:reviewvocabcurrent'))
#         else:
#             return JsonResponse(loop_data)
#     else:
#         messages.add_message(request, messages.ERROR, error_finish)
#         return JsonResponse(error_data)


class ReviewVocabCurrentView(LoginRequiredMixin, ListView):
    template_name = 'main/vocabq_review_current.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewVocabCurrentView, self).get_context_data(**kwargs)
        currentchapter = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentchapter'] = currentchapter
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        return VocabRecord.objects.filter(user_id=self.request.user.id).exclude(next_review__isnull=True).order_by('next_review')[:10]


class ReviewExpressionView(LoginRequiredMixin, TemplateView):
    template_name = 'main/expressionq_review.html'


@require_http_methods(["POST"])
def reviewexpressionsave(request):
    er_queryset = ExpressionRecord.objects.filter(user_id=request.user.id, next_review__lte=datetime.now())
    erupdate = ExpressionRecordSerializer(er_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
    if erupdate.is_valid():
        erupdate.save()
        return JsonResponse(save_data)
    else:
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)


# @require_http_methods(["POST"])
# def reviewexpressionfinish(request):
#     er_queryset = ExpressionRecord.objects.filter(user_id=request.user.id, next_review__lte=datetime.now())
#     erupdate = ExpressionRecordSerializer(er_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
#     if erupdate.is_valid():
#         erupdate.save()
#         erecords = ExpressionRecord.objects.filter(user_id=request.user.id, next_review__lte=datetime.now())[:10]
#         if erecords is None:
#             return HttpResponseRedirect(reverse('main:reviewexpressioncurrent'))
#         else:
#             return JsonResponse(loop_data)
#     else:
#         messages.add_message(request, messages.ERROR, error_finish)
#         return JsonResponse(error_data)


class ReviewExpressionCurrentView(LoginRequiredMixin, ListView):
    template_name = 'main/expressionq_review_current.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewExpressionCurrentView, self).get_context_data(**kwargs)
        currentchapter = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentchapter'] = currentchapter
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        return ExpressionRecord.objects.filter(user_id=self.request.user.id).exclude(next_review__isnull=True).order_by('next_review')[:10]


class ReviewSentenceView(LoginRequiredMixin, TemplateView):
    template_name = 'main/sentenceq_review.html'


@require_http_methods(["POST"])
def reviewsentencesave(request):
    sr_queryset = SentenceRecord.objects.filter(user_id=request.user.id, next_review__lte=datetime.now())
    srupdate = SentenceRecordSerializer(sr_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
    if srupdate.is_valid():
        srupdate.save()
        return JsonResponse(save_data)
    else:
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)


# @require_http_methods(["POST"])
# def reviewsentencefinish(request):
#     sr_queryset = SentenceRecord.objects.filter(user_id=request.user.id, next_review__lte=datetime.now())
#     srupdate = SentenceRecordSerializer(sr_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
#     if srupdate.is_valid():
#         srupdate.save()
#         srecords = SentenceRecord.objects.filter(user_id=request.user.id, next_review__lte=datetime.now())[:10]
#         if srecords is None:
#             return HttpResponseRedirect(reverse('main:reviewsentencecurrent'))
#         else:
#             return JsonResponse(loop_data)
#     else:
#         messages.add_message(request, messages.ERROR, error_finish)
#         return JsonResponse(error_data)


class ReviewSentenceCurrentView(LoginRequiredMixin, ListView):
    template_name = 'main/sentenceq_review_current.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewSentenceCurrentView, self).get_context_data(**kwargs)
        currentchapter = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentchapter'] = currentchapter
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        return SentenceRecord.objects.filter(user_id=self.request.user.id).exclude(next_review__isnull=True).order_by('next_review')[:10]


class ReviewFlashcardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/flashcardq_review.html'


@require_http_methods(["POST"])
def reviewflashcardsave(request):
    fr_queryset = Flashcard.objects.filter(user_id=request.user.id, next_review__lte=datetime.now())
    frupdate = FlashcardSerializer(fr_queryset, data=json.loads(request.POST.get('qdata')), partial=True, many=True)
    if frupdate.is_valid():
        frupdate.save()
        return JsonResponse(save_data)
    else:
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)


class ReviewFlashcardCurrentView(LoginRequiredMixin, ListView):
    template_name = 'main/flashcardq_review_current.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewFlashcardCurrentView, self).get_context_data(**kwargs)
        currentchapter = get_object_or_404(Chapter, pk=self.request.user.profile.currentchapter)
        context['currentchapter'] = currentchapter
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        return Flashcard.objects.filter(user_id=self.request.user.id).order_by('next_review')[:10]


# #################################################################################
# ################################ END REVIEWS ####################################
# #################################################################################

# #################################################################################
# ################################ EXERCISES ######################################
# #################################################################################

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


class PassageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/exercise_passage.html'

    def get_context_data(self, **kwargs):
        context = super(PassageView, self).get_context_data(**kwargs)
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


@require_http_methods(["POST"])
def passagefinish(request, chapter_id, exercise_id):
    if request.user.profile.currentexercise < int(exercise_id):
        return JsonResponse(error_data)
    else:
        form = ValidateExerciseFinish(request.POST)
        if form.is_valid():
            q = form.cleaned_data['q']
            totalq = form.cleaned_data['totalq']
            score = form.cleaned_data['score']
            if q == totalq == ExerciseSentence.objects.filter(exercise_id__exact=exercise_id).count():
                er_id = ExerciseRecord.objects.get(user_id=request.user.id, exercise__id__exact=exercise_id).id
                if er_id:
                    ExerciseRecord.update_score(er_id, score, request.user)
                    return HttpResponseRedirect(reverse('main:passagesuccess', kwargs={'chapter_id': chapter_id, 'exercise_id': exercise_id}))
                else:
                    messages.add_message(request, messages.ERROR, error_finish)
                    return JsonResponse(error_data)
            else:   # if # of questions doesn't line up
                messages.add_message(request, messages.ERROR, error_finish)
                return JsonResponse(error_data)
        else:   # if form is not valid
            messages.add_message(request, messages.ERROR, error_finish)
            return JsonResponse(error_data)


class PassageSuccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/exercise_passage_success.html'

    def get_context_data(self, **kwargs):
        context = super(PassageSuccessView, self).get_context_data(**kwargs)
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


class DialogueView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/exercise_dialogue.html'

    def get_context_data(self, **kwargs):
        context = super(DialogueView, self).get_context_data(**kwargs)
        exercise = get_object_or_404(Exercise, pk=self.kwargs['exercise_id'])
        context['exercise'] = exercise
        context['chapter'] = exercise.chapter
        context['pieces'] = exercise.exercise_pieces()
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['exercise_id']) <= self.request.user.profile.currentexercise:
            return True


@require_http_methods(["POST"])
def dialoguefinish(request, chapter_id, exercise_id):
    if request.user.profile.currentexercise < int(exercise_id):
        return JsonResponse(error_data)
    else:
        form = ValidateExerciseFinish(request.POST)
        if form.is_valid():
            q = form.cleaned_data['q']
            totalq = form.cleaned_data['totalq']
            score = form.cleaned_data['score']
            if q == totalq == ExercisePrompt.objects.filter(exercise_id__exact=exercise_id).count():
                er_id = ExerciseRecord.objects.get(user_id=request.user.id, exercise__id__exact=exercise_id).id
                if er_id:
                    ExerciseRecord.update_score(er_id, score, request.user)
                    return HttpResponseRedirect(reverse('main:dialoguesuccess', kwargs={'chapter_id': chapter_id, 'exercise_id': exercise_id}))
                else:
                    messages.add_message(request, messages.ERROR, error_finish)
                    return JsonResponse(error_data)
            else:   # if # of prompts doesn't line up
                messages.add_message(request, messages.ERROR, error_finish)
                return JsonResponse(error_data)
        else:   # if form is not valid
            messages.add_message(request, messages.ERROR, error_finish)
            return JsonResponse(error_data)


class DialogueSuccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/exercise_dialogue_success.html'

    def get_context_data(self, **kwargs):
        context = super(DialogueSuccessView, self).get_context_data(**kwargs)
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

# #################################################################################
# ############################ END EXERCISES ######################################
# #################################################################################

class FlashcardListView(LoginRequiredMixin, ListView):
    template_name = 'main/flashcard_list.html'

    def get_queryset(self):
        queryset = Flashcard.objects.filter(user_id=self.request.user.id)
        return queryset

class FlashcardCreateView(LoginRequiredMixin, CreateView):
    model = Flashcard
    template_name = 'main/flashcard_new.html'
    form_class = FlashcardForm
    success_url = reverse_lazy('main:flashcard')

    def form_valid(self, form):
        # form.instance.user = Profile.objects.get(user=self.request.user)
        # form.instance.created_by = self.request.user
        form.instance.user = self.request.user
        return super().form_valid(form)

class FlashcardUpdateView(LoginRequiredMixin, UpdateView):
    model = Flashcard
    template_name = 'main/flashcard_update.html'
    form_class = FlashcardForm
    success_url = reverse_lazy('main:flashcard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # form.instance.created_by = self.request.user
        return super().form_valid(form)

class FlashcardDeleteView(LoginRequiredMixin, DeleteView):
    model = Flashcard
    template_name = 'main/flashcard_delete.html'
    success_url = reverse_lazy('main:flashcard')

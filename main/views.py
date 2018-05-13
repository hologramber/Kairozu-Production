from itertools import chain

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile, Expression, ExpressionRecord, Vocabulary, Lesson, Chapter, VocabRecord, SentenceRecord, Exercise, ExerciseRecord, ExerciseSentence, GrammarNote


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
    template_name = 'main/vocabquiz.html'

    def get_context_data(self, **kwargs):
        context = super(VocabQuizView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def test_func(self, **kwargs):
        if int(self.kwargs['chapter_id']) <= self.request.user.profile.currentvocab:
            return True


# assign vocab code depending if vocab quiz submission was correct or not
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

# #################################################################################
# ############################# END EXPRESSIONS ###################################
# #################################################################################

# #################################################################################
# ############################# PRACTICES #########################################
# #################################################################################

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

# #################################################################################
# ############################### END PRACTICES ###################################
# #################################################################################

# #################################################################################
# ############################### SENTENCES #######################################
# #################################################################################

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

# #################################################################################
# ################################ END SENTENCES ##################################
# #################################################################################

# #################################################################################
# ################################ REVIEWS ########################################
# #################################################################################

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
        return VocabRecord.objects.filter(user_id=self.request.user.id).exclude(next_review__isnull=True).order_by('next_review')[:10]


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
        return SentenceRecord.objects.filter(user_id=self.request.user.id).exclude(next_review__isnull=True).order_by('next_review')[:10]


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
        return ExpressionRecord.objects.filter(user_id=self.request.user.id).exclude(next_review__isnull=True).order_by('next_review')[:10]

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

# #################################################################################
# ############################ END EXERCISES ######################################
# #################################################################################
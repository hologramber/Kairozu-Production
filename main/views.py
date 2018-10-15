import json
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Vocabulary, Practice, Sentence, Lesson, Chapter, GrammarNote, Flashcard
from .forms import ValidateFinishForm, FlashcardForm
from .serializers import FlashcardSerializer

error_finish = 'There was a problem with saving your current progress. Please e-mail kairozu@kairozu.com if you suspect this is an error.'
loop_finish = 'You\'ve successfully completed this quiz; it will loop for as long as you\'d like to practice.'
error_data = {'error': True}
loop_data = {'loop': True}
save_data = {'save': True}

# where users enter chapters; grid of red sun chapters/progress
class MainView(ListView):
    model = Chapter
    template_name = 'main/main.html'


# front interface for each chapter (prior to entering vocab/grammar/etc)
class ChapterInterfaceView(ListView):
    template_name = 'main/interface.html'

    def get_context_data(self, **kwargs):
        context = super(ChapterInterfaceView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter_now = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        return Lesson.objects.filter(chapter=chapter_now)

# interface for each grammar point (title + grammar + point + examples + more info)
class LessonView(TemplateView):
    template_name = 'main/lesson.html'

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['lesson'] = lesson
        context['chapter'] = lesson.chapter
        context['pieces'] = lesson.lesson_pieces()
        return context


class GrammarNoteView(TemplateView):
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


class SummaryView(ListView):
    template_name = 'main/summary.html'

    def get_context_data(self, **kwargs):
        context = super(SummaryView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter_now = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        return Lesson.objects.filter(chapter=chapter_now)


# #################################################################################
# ################################## VOCABULARY ###################################
# #################################################################################

# list of vocabulary per chapter
class VocabListView(ListView):
    template_name = 'main/vocablist.html'

    def get_context_data(self, **kwargs):
        context = super(VocabListView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context

    def get_queryset(self):
        chapter_now = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        return Vocabulary.objects.filter(chapter=chapter_now)


# vocabulary quiz first-load (future loads aren't full refreshes)
class VocabQuizView(TemplateView):
    template_name = 'main/vocabq.html'

    def get_context_data(self, **kwargs):
        context = super(VocabQuizView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        return context


@require_http_methods(["POST"])
def vocabfinish(request, chapter_id):
    form = ValidateFinishForm(request.POST)
    if form.is_valid():
        q = form.cleaned_data['q']
        totalq = form.cleaned_data['totalq']
        if q == totalq == Vocabulary.objects.filter(chapter_id__exact=chapter_id).count():
            return HttpResponseRedirect(reverse('main:vocabsuccess', kwargs={'chapter_id': chapter_id}))
        else:
            messages.add_message(request, messages.ERROR, error_finish)
            return JsonResponse(error_data)
    else:
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)


class VocabSuccessView(TemplateView):
    template_name = 'main/success.html'

    def get_context_data(self, **kwargs):
        context = super(VocabSuccessView, self).get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['chapter_id'])
        context['chapter'] = chapter
        context['which_success'] = chapter.title + " Vocabulary Quiz."
        context['chapter_all'] = Chapter.objects.all()
        return context


# #################################################################################
# ############################## END VOCABULARY ###################################
# #################################################################################

# #################################################################################
# ############################# PRACTICES #########################################
# #################################################################################

# practice quiz first-load (future loads aren't full refreshes)
class PracticeQuizView(TemplateView):
    template_name = 'main/practiceq.html'

    def get_context_data(self, **kwargs):
        context = super(PracticeQuizView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['chapter'] = lesson.chapter
        context['lesson'] = lesson
        return context


@require_http_methods(["POST"])
def practicefinish(request, lesson_id):
    form = ValidateFinishForm(request.POST)
    if form.is_valid():
        q = form.cleaned_data['q']
        totalq = form.cleaned_data['totalq']
        if q == totalq == Practice.objects.filter(lesson_id__exact=lesson_id).count():
            return HttpResponseRedirect(reverse('main:practicesuccess', kwargs={'lesson_id': lesson_id}))
        else:   # if # of questions doesn't line up
            messages.add_message(request, messages.ERROR, error_finish)
            return JsonResponse(error_data)
    else:   # if form is not valid
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)


class PracticeSuccessView(TemplateView):
    template_name = 'main/success.html'

    def get_context_data(self, **kwargs):
        context = super(PracticeSuccessView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['lesson'] = lesson
        context['which_success'] = "Practice Quiz for \"" + lesson.title + "\""
        context['chapter'] = lesson.chapter
        context['chapter_all'] = Chapter.objects.all()
        return context


# #################################################################################
# ############################### END PRACTICES ###################################
# #################################################################################

# #################################################################################
# ############################### SENTENCES #######################################
# #################################################################################

# sentence quiz first-load (future loads aren't full refreshes)
class SentenceQuizView(TemplateView):
    template_name = 'main/sentenceq.html'

    def get_context_data(self, **kwargs):
        context = super(SentenceQuizView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['chapter'] = lesson.chapter
        context['lesson'] = lesson
        return context


@require_http_methods(["POST"])
def sentencefinish(request, lesson_id):
    form = ValidateFinishForm(request.POST)
    if form.is_valid():
        q = form.cleaned_data['q']
        totalq = form.cleaned_data['totalq']
        if q == totalq == Sentence.objects.filter(lesson_id__exact=lesson_id).count():
            return HttpResponseRedirect(reverse('main:sentencesuccess', kwargs={'lesson_id': lesson_id}))
        else:
            messages.add_message(request, messages.ERROR, error_finish)
            return JsonResponse(error_data)
    else:
        messages.add_message(request, messages.ERROR, error_finish)
        return JsonResponse(error_data)


class SentenceSuccessView(TemplateView):
    template_name = 'main/success.html'

    def get_context_data(self, **kwargs):
        context = super(SentenceSuccessView, self).get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        context['which_success'] = "Sentence Quiz for \"" + lesson.title + "\""
        context['chapter'] = lesson.chapter
        context['chapter_all'] = Chapter.objects.all()
        return context


# #################################################################################
# ################################ END SENTENCES ##################################
# #################################################################################

# #################################################################################
# ################################ REVIEWS ########################################
# #################################################################################

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

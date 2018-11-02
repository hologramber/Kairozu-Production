import json, csv
from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Vocabulary, Practice, Sentence, Lesson, Chapter, GrammarNote, Flashcard, FlashcardSet
from .forms import ValidateFinishForm, FlashcardForm, FlashcardSetForm, FlashcardFromVocabForm, FlashcardFromQuizForm, FlashcardDeleteBySet
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
        if self.request.user.is_authenticated:
            Profile.has_reviews(self.request.user)
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
        if self.request.user.is_authenticated:
            Profile.has_reviews(self.request.user)
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
        if self.request.user.is_authenticated:
            Profile.has_reviews(self.request.user)
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
        if self.request.user.is_authenticated:
            Profile.has_reviews(self.request.user)
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
        if self.request.user.is_authenticated:
            Profile.has_reviews(self.request.user)
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
        if self.request.user.is_authenticated:
            Profile.has_reviews(self.request.user)
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
        if self.request.user.is_authenticated:
            Profile.has_reviews(self.request.user)
        return context


# #################################################################################
# ################################ END SENTENCES ##################################
# #################################################################################

# #################################################################################
# ################################ REVIEWS ########################################
# #################################################################################

class ReviewFlashcardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/flashcardq_review.html'


class ReviewFlashcardQuickView(LoginRequiredMixin, TemplateView):
    template_name = 'main/flashcardq_review_quick.html'


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
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        return Flashcard.objects.filter(user_id=self.request.user.id).order_by('next_review')[:10]


# #################################################################################
# ################################ END REVIEWS ####################################
# #################################################################################

class FlashcardSetListView(LoginRequiredMixin, ListView):
    template_name = 'main/flashcardset_list.html'

    def get_context_data(self, **kwargs):
        context = super(FlashcardSetListView, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        queryset = FlashcardSet.objects.filter(user_id=self.request.user.id)
        return queryset


class FlashcardSetDetailView(LoginRequiredMixin, ListView):
    template_name = 'main/flashcardset_list_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FlashcardSetDetailView, self).get_context_data(**kwargs)
        fset = get_object_or_404(FlashcardSet, slug=self.kwargs['slug'])
        context['fset'] = fset
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        queryset = Flashcard.objects.filter(set__slug__exact=self.kwargs['slug'])
        return queryset


class FlashcardSetCreateView(LoginRequiredMixin, CreateView):
    model = FlashcardSet
    template_name = 'main/flashcardset_create.html'
    form_class = FlashcardSetForm
    success_url = reverse_lazy('main:flashcardsetlist')

    def form_valid(self, form):
        # form.instance.user = Profile.objects.get(user=self.request.user)
        # form.instance.created_by = self.request.user
        form.instance.user = self.request.user
        return super().form_valid(form)


class FlashcardSetUpdateView(LoginRequiredMixin, UpdateView):
    model = FlashcardSet
    template_name = 'main/flashcard_create.html'
    form_class = FlashcardSetForm
    success_url = reverse_lazy('main:flashcardsetlist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # form.instance.created_by = self.request.user
        return super().form_valid(form)


class FlashcardSetDeleteView(LoginRequiredMixin, DeleteView):
    model = FlashcardSet
    template_name = 'main/flashcardset_delete.html'
    success_url = reverse_lazy('main:flashcardsetlist')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.name != "default":
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(request, messages.ERROR, "Cannot delete the default flashcard set.")
            return HttpResponseRedirect(self.get_success_url())

class FlashcardListViewAll(LoginRequiredMixin, ListView):
    template_name = 'main/flashcard_list_all.html'

    def get_context_data(self, **kwargs):
        context = super(FlashcardListViewAll, self).get_context_data(**kwargs)
        Profile.has_reviews(self.request.user)
        return context

    def get_queryset(self):
        queryset = FlashcardSet.objects.filter(user_id=self.request.user.id)
        return queryset


class FlashcardCreateView(LoginRequiredMixin, CreateView):
    model = Flashcard
    template_name = 'main/flashcard_create.html'
    form_class = FlashcardForm

    def get_initial(self):
      slug = self.kwargs['slug']
      set = FlashcardSet.objects.filter(slug__exact=slug).first()
      return {
        'set': set,
      }

    def form_valid(self, form):
        # form.instance.user = Profile.objects.get(user=self.request.user)
        # form.instance.created_by = self.request.user
        form.instance.user = self.request.user
        form.instance.set = FlashcardSet.objects.filter(slug__exact=self.kwargs['slug']).first()
        return super().form_valid(form)

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'default-' + self.request.user.id
        return reverse('main:flashcardsetdetail', kwargs={'slug': slug})

class FlashcardUpdateView(LoginRequiredMixin, UpdateView):
    model = Flashcard
    template_name = 'main/flashcard_create.html'
    form_class = FlashcardForm
    pk_url_kwarg = "card_id"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.set = FlashcardSet.objects.filter(slug__exact=self.kwargs['slug']).first()
        # form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'default-' + self.request.user.id
        return reverse('main:flashcardsetdetail', kwargs={'slug': slug})

class FlashcardDeleteView(LoginRequiredMixin, DeleteView):
    model = Flashcard
    template_name = 'main/flashcard_delete.html'
    pk_url_kwarg = "card_id"

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'default-' + self.request.user.id
        return reverse('main:flashcardsetdetail', kwargs={'slug': slug})

@login_required
def flashcard_batch_csv(request):
    data = {}
    availsets = FlashcardSet.objects.filter(user_id__exact=request.user.id)
    if "GET" == request.method:
        return render(request, "main/flashcard_batch_csv.html", {'data': data, 'availsets': availsets})
    # if not GET, then proceed
    try:
        savetoset_id = request.POST["desiredSet"]
        savetoset = FlashcardSet.objects.get(id=savetoset_id)
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'Uploaded file isn\'t a CSV (comma separated value) file.')
            return HttpResponseRedirect(reverse("main:flashcardbatch"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("main:flashcardbatch"))

        csv_reader = csv.reader((x.decode("utf-8") for x in csv_file.readlines()), delimiter=',')

        # file_data = csv_file.read().decode("utf-8")
        # lines = file_data.split("\n")
        importsuccess = True
        #loop over the lines and save them in db. If error , store as string and then display
        for line in csv_reader:
            # fields = line.split(",")
            data_dict = {}
            # ['english', 'set', 'kana', 'kanji', 'strict', 'literal', 'context', 'note']

            data_dict["english"] = line[0]
            data_dict["set"] = savetoset.id
            data_dict["kana"] = line[1]
            data_dict["kanji"] = line[2]
            data_dict["strict"] = line[3]
            data_dict["literal"] = line[4]
            data_dict["context"] = line[5]
            data_dict["note"] = line[6]
            try:
                form = FlashcardForm(data_dict)
                form.instance.user = request.user
                if form.is_valid():
                    form.save()
                else:
                    importsuccess = False
            except Exception as e:
                messages.error(request, "Unable to save card. " + repr(e))
                pass
        if importsuccess:
            messages.add_message(request, messages.SUCCESS, 'Flashcards successfully imported!')
        else:
            messages.add_message(request, messages.ERROR, 'There was a problem with flashcard import. Contact kairozu@kairozu.com for assistance.')
    except Exception as e:
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("main:flashcardbatch"))


@login_required
def flashcard_from_vocab(request):
    chapters = Chapter.objects.all()
    sets = FlashcardSet.objects.filter(user_id__exact=request.user.id)
    if "GET" == request.method:
        return render(request, "main/flashcard_from_vocab.html", {'sets': sets, 'chapters': chapters})
    elif request.method == 'POST':
        new_cards_from_vocab = FlashcardFromVocabForm(request.POST)
        if new_cards_from_vocab.is_valid():
            from_chapter = new_cards_from_vocab.cleaned_data['desiredChapter']
            to_set = new_cards_from_vocab.cleaned_data['desiredSet']
            vocabs = Vocabulary.objects.filter(chapter_id__exact=from_chapter)
            targetset = FlashcardSet.objects.get(id=to_set)
            for vocab in vocabs:
                flashcard = Flashcard()
                flashcard.user = request.user
                flashcard.set = targetset
                flashcard.strict = True
                flashcard.english = vocab.english
                flashcard.kana = vocab.kana
                flashcard.kanji = vocab.kanji
                flashcard.context = vocab.context
                flashcard.save()
            messages.add_message(request, messages.SUCCESS, 'Flashcards successfully imported!')
            return HttpResponseRedirect(reverse('main:flashcardsetdetail', kwargs={'slug': targetset.slug }))
        else:
            messages.add_message(request, messages.ERROR, 'There was a problem with flashcard import. Contact kairozu@kairozu.com for assistance.')
            return HttpResponseRedirect(reverse('main:flashcardfromvocab'))


@login_required
def flashcard_from_quiz(request):
    lessons = Lesson.objects.all()
    sets = FlashcardSet.objects.filter(user_id__exact=request.user.id)
    if "GET" == request.method:
        return render(request, "main/flashcard_from_quiz.html", {'sets': sets, 'lessons': lessons})
    elif request.method == 'POST':
        new_cards_from_quiz = FlashcardFromQuizForm(request.POST)
        if new_cards_from_quiz.is_valid():
            from_lesson = new_cards_from_quiz.cleaned_data['desiredLesson']
            to_set = new_cards_from_quiz.cleaned_data['desiredSet']
            sentences = Sentence.objects.filter(lesson_id__exact=from_lesson)
            targetset = FlashcardSet.objects.get(id=to_set)
            for sentence in sentences:
                flashcard = Flashcard()
                flashcard.user = request.user
                flashcard.set = targetset
                flashcard.strict = sentence.strict
                flashcard.english = sentence.english
                flashcard.kana = sentence.kana
                flashcard.kanji = sentence.kanji
                flashcard.literal = sentence.literal
                flashcard.context = sentence.context
                flashcard.disamb_location = sentence.disamb_location
                flashcard.save()

            messages.add_message(request, messages.SUCCESS, 'Flashcards successfully imported!')
            return HttpResponseRedirect(reverse('main:flashcardsetdetail', kwargs={'slug': targetset.slug }))
        else:
            messages.add_message(request, messages.ERROR, 'There was a problem with flashcard import. Contact kairozu@kairozu.com for assistance.')
            return HttpResponseRedirect(reverse('main:flashcardfromvocab'))


@login_required
def flashcard_delete_by_set(request):
    sets = FlashcardSet.objects.filter(user_id__exact=request.user.id)
    if "GET" == request.method:
        return render(request, "main/flashcard_delete_by_set.html", {'sets': sets})
    elif request.method == 'POST':
        new_cards_from_quiz = FlashcardDeleteBySet(request.POST)
        if new_cards_from_quiz.is_valid():
            delete_from_set = new_cards_from_quiz.cleaned_data['desiredSet']
            flashcards = Flashcard.objects.filter(set_id=delete_from_set)
            for flashcard in flashcards:
                flashcard.delete()

            messages.add_message(request, messages.SUCCESS, 'Flashcards successfully deleted.')
            return HttpResponseRedirect(reverse('main:flashcardsetlist'))
        else:
            messages.add_message(request, messages.ERROR, 'There was a problem with flashcard import. Contact kairozu@kairozu.com for assistance.')
            return HttpResponseRedirect(reverse('main:flashcardsetlist'))
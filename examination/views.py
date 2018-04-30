from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .models import Examination, QuestionSet, UserChoice
import re


class ExaminationListView(LoginRequiredMixin, ListView):
    paginate_by = 20

    def get_queryset(self):
        return Examination.objects.filter(user=self.request.user).order_by('-start_time')


class ExaminationDetailView(LoginRequiredMixin, DetailView):
    question_prefix = 'question'

    def get_queryset(self):
        return Examination.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ExaminationDetailView, self).get_context_data(**kwargs)
        context['user_choices'] = kwargs.get('user_choices') or self.get_user_choices(self.object, self.request.user)
        return context

    def post(self, request, pk):
        self.object = self.get_object()

        self.save_user_choices()

        is_submit = self.request.POST.get('submit')
        if is_submit == 'true':
            self.submit_examination()

        user_choices = self.get_user_choices(self.object, self.request.user)
        return self.render_to_response(self.get_context_data(user_choices=user_choices))

    def submit_examination(self):
        self.object.finish_time = timezone.now()
        self.object.save()

    def save_user_choices(self):
        posted_user_choices = self.get_user_choices_from_form(self.request.POST)
        self.update_user_choices(posted_user_choices)

    def get_user_choices_from_form(self, form_data):
        user_choices = {}
        for key in form_data.keys():
            question_id = self.get_question_id_from_key(key)
            if question_id and self.object.question_set.questions.filter(id=question_id).exists():
                choice_id = self.get_choice_id_from_form(form_data, question_id)
                if choice_id:
                    user_choices[question_id] = choice_id
        return user_choices

    def get_question_id_from_key(self, key):
        pattern = r'^{}_(\d+)$'.format(self.question_prefix)
        match = re.match(pattern, key)
        if match:
            return match.groups()[0]
        else:
            return None

    def update_user_choices(self, user_choices):
        for question_id, choice_id in user_choices.items():
            UserChoice.objects.update_or_create(examination=self.object, question_id=question_id,
                                                user=self.request.user,
                                                defaults={'choice_id': choice_id})

    def get_choice_id_from_form(self, form_data, question_id):
        key = '{}_{}'.format(self.question_prefix, question_id)
        return form_data.get(key)

    def get_user_choices(self, examination, user):
        return {str(user_choice.choice.question_id): str(user_choice.choice.id)
                for user_choice in UserChoice.objects.filter(examination=examination, user=user)}


class ExaminationCreateView(LoginRequiredMixin, View):
    def post(self, request):
        question_set = self.get_quetion_set(request)
        return self.create_examination(question_set, request.user)

    def get_quetion_set(self, request):
        question_set_id = request.POST.get('question_set')
        if not question_set_id:
            raise Http404()

        question_set = get_object_or_404(QuestionSet, is_published=True, id=question_set_id)
        return question_set

    def to_examination(self, examination):
        return redirect('examination-detail', pk=examination.pk)

    def create_examination(self, question_set, user):
        examination, created = Examination.objects.get_or_create(user=user, question_set=question_set,
                                                                 finish_time__isnull=True)
        return self.to_examination(examination)

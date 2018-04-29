from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from .models import Examination, QuestionSet


class ExaminationListView(LoginRequiredMixin, ListView):
    paginate_by = 20

    def get_queryset(self):
        return Examination.objects.filter(user=self.request.user)


class ExaminationDetailView(LoginRequiredMixin, DetailView):
    paginate_by = 20

    def get_queryset(self):
        return Examination.objects.filter(user=self.request.user)


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
        examination, created = Examination.objects.get_or_create(user=user, question_set=question_set, finish_time__isnull=True)
        return self.to_examination(examination)

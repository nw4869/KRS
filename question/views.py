from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import QuestionSet


class QuestionSetListView(LoginRequiredMixin, ListView):
    queryset = QuestionSet.objects.filter(is_published=True).order_by('-created_time')
    paginate_by = 20


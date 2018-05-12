from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import QuestionSet


class QuestionSetListView(LoginRequiredMixin, ListView):
    queryset = QuestionSet.objects.filter(is_published=True).order_by('-created_time')
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionSetListView, self).get_context_data(object_list=object_list, **kwargs)
        context['title'] = '测试题集'
        return context


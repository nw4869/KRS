from django.db import models
from question.models import QuestionSet, ChoiceQuestion, Choice
from django.conf import settings


class Examination(models.Model):
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def is_finished(self):
        return self.finish_time is not None

    def __str__(self):
        return 'QS: {}, user: {}, start_time: {}'.format(self.question_set.name,
                                                         self.user,
                                                         self.start_time)


class UserChoice(models.Model):
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return 'user: {}, choice: {}, examination: {}'.format(self.user, self.choice, self.examination.question_set.name)
from django.db import models


class ChoiceQuestion(models.Model):
    # examination = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    content = models.CharField(max_length=10000)
    answer = models.ForeignKey('question.Choice', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.content


class Choice(models.Model):
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

    def __str__(self):
        return 'C: {} (Q: {})'.format(self.content, self.question.content)


class QuestionSet(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=10000)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    questions = models.ManyToManyField(ChoiceQuestion)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

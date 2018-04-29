from django.contrib import admin
from .models import *

admin.site.register(ChoiceQuestion)
admin.site.register(Choice)
admin.site.register(QuestionSet)

from django.contrib import admin
from .models import *


class ExaminationAdmin(admin.ModelAdmin):
    readonly_fields = ('start_time',)


admin.site.register(Examination, ExaminationAdmin)
admin.site.register(UserChoice)

"""pig URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from account.views import RegisterView
from examination.views import ExaminationListView, ExaminationDetailView, ExaminationCreateView
from question.views import QuestionSetListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', RegisterView.as_view(), name='register'),

    path('question/', QuestionSetListView.as_view(), name='questionset-list'),

    path('examination/', ExaminationListView.as_view(), name='examination-list'),
    path('examination/start', ExaminationCreateView.as_view(), name='examination-create'),
    path('examination/<int:pk>', ExaminationDetailView.as_view(), name='examination-detail'),

    path('', TemplateView.as_view(template_name='home.html', extra_context={'title': '欢迎使用在线知识点测评系统'}), name='home')
]

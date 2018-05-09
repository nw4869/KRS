from django import forms
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='邮箱', max_length=200, help_text='必填。')

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        rtn = super(RegisterView, self).form_valid(form)

        # login user
        user = self.object
        login(self.request, user)

        return rtn

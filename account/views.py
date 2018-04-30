from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        rtn = super(RegisterView, self).form_valid(form)

        # login user
        user = self.object
        login(self.request, user)

        return rtn

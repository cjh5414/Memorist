from django.views.generic import *

from account.forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = '/login/'
    template_name = 'signup.html'


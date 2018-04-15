from django import forms
from django.forms import ModelForm
from account.models import User


class SignUpForm(ModelForm):
    password1 = forms.CharField()
    password2 = forms.CharField()

    def clean_password2(self):
        # Passwords must match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The two password fields didn\'t match.')
        return password2

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


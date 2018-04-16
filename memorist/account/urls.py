from django.conf.urls import url
from django.contrib.auth.views import LoginView

from account.views import SignUpView

app_name = 'account'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^signup/$', SignUpView.as_view(template_name='signup.html'), name='signup'),
]

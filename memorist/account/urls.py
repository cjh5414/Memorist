from django.conf.urls import url
from django.contrib.auth.views import LoginView

app_name = 'account'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
]

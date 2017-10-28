from django.conf.urls import url

from . import views

app_name = 'rental'

urlpatterns = [
    url(r'^words/add/$', views.WordAddView.as_view(), name='add_word'),
]

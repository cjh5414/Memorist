from django.conf.urls import url

from . import views

app_name = 'rental'

urlpatterns = [
    url(r'^words/add/$', views.WordAddView.as_view(), name='add_word'),
    url(r'^words/$', views.WordListView.as_view(), name='word_list'),
    url(r'^translate/$', views.WordTranslate.as_view(), name='word_translate'),
]

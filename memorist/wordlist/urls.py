from django.conf.urls import url

from . import views

app_name = 'rental'

urlpatterns = [
    url(r'^words/$', views.WordListView.as_view(), name='word_list'),
    url(r'^words/add/$', views.WordAddView.as_view(), name='add_word'),
    url(r'^words/(?P<pk>[0-9]+)/delete/$', views.WordDeleteView.as_view(), name='delete_word'),
    url(r'^translate/$', views.WordTranslate.as_view(), name='word_translate'),
    url(r'^study/$', views.WordStudy.as_view(), name='word_study'),
]

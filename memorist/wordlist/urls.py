from django.conf.urls import url

from . import views

app_name = 'wordlist'

urlpatterns = [
    url(r'^words/$', views.WordListView.as_view(), name='word_list'),
    url(r'^words/add/$', views.WordAddView.as_view(), name='add_word'),
    url(r'^words/deleted/$', views.DeletedWordListView.as_view(), name='deleted_word_list'),
    url(r'^words/(?P<pk>[0-9]+)/delete/$', views.WordDeleteView.as_view(), name='delete_word'),
    url(r'^words/(?P<pk>[0-9]+)/restore/$', views.WordRestore.as_view(), name='restore_word'),
    url(r'^words/(?P<pk>[0-9]+)/edit/$', views.WordEdit.as_view(), name='edit_word'),
    url(r'^translate/$', views.WordTranslate.as_view(), name='word_translate'),
    url(r'^study/$', views.WordStudy.as_view(), name='word_study'),
    url(r'^study/next/$', views.WordStudyNext.as_view(), name='word_study_next'),
    url(r'^study/test/$', views.MakeTest.as_view(), name='make_test'),
    url(r'^study/numberofwords/$', views.GetNumOfWords.as_view(), name='get_num_of_words'),
    url(r'^study/progress/$', views.GetStudyProgress.as_view(), name='get_study_progress'),
    url(r'^pronounce/$', views.Pronounce.as_view(), name='pronounce'),
]

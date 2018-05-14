from django.conf.urls import url

from study.views import *

app_name = 'study'

urlpatterns = [
    url(r'^question-type-change/', QuestionTypeChangeView.as_view(), name='question_type_change'),
]

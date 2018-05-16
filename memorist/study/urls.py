from django.conf.urls import url

from study.views import *

app_name = 'study'

urlpatterns = [
    url(r'^question-type-change/', QuestionTypeChangeView.as_view(), name='question_type_change'),
    url(r'^chosen-days-change/', ChosenDaysChangeView.as_view(), name='chosen_days_change'),
    url(r'^status/', GetStatus.as_view(), name='get_status'),
]

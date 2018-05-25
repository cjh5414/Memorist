from django.conf.urls import url

from studystatus.views import *

app_name = 'study'

urlpatterns = [
    url(r'^update-question-type/', UpdateQuestionTypeView.as_view(), name='update_question_type'),
    url(r'^update-chosen-days/', UpdateChosenDaysView.as_view(), name='update_chosen_days'),
    url(r'^', GetStatus.as_view(), name='get_status'),
]

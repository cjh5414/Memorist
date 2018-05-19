from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class QuestionTypeChangeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request.user.study.question_type = self.request.POST['question_type']
        request.user.save()

        return JsonResponse({'result': 'Success'})


class ChosenDaysChangeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request.user.study.chosen_days = self.request.POST['chosen_days']
        request.user.save()

        return JsonResponse({'result': 'Success'})


class GetStatus(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        study = request.user.study

        return JsonResponse({
            'question_type': study.question_type,
            'chosen_days': study.chosen_days,
        })

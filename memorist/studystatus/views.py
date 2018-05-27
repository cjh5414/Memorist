from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class UpdateQuestionTypeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request.user.studystatus.question_type = self.request.POST['question_type']
        request.user.save()

        return JsonResponse({'result': 'Success'})


class UpdateChosenDaysView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request.user.studystatus.chosen_days = self.request.POST['chosen_days']
        request.user.save()

        return JsonResponse({'result': 'Success'})


class GetStatus(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        studystatus = request.user.studystatus

        return JsonResponse({
            'question_type': studystatus.question_type,
            'chosen_days': studystatus.chosen_days,
        })

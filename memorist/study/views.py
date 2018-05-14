from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class QuestionTypeChangeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request.user.study.question_type = self.request.POST['question_type']
        request.user.study.save()
        request.user.save()

        return JsonResponse({'result': 'Success'})

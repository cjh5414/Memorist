from django.views import View
from django.shortcuts import render


class WordAddView(View):
    template_name = 'add_word.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

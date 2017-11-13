import os
import json
import urllib.request

from django.views import View
from django.shortcuts import render
from django.views.generic import *
from django.http import JsonResponse, HttpResponseRedirect

from wordlist.forms import WordAddForm
from wordlist.models import Word


class WordAddView(FormView):
    form_class = WordAddForm
    template_name = 'add_word.html'
    success_url = '/words/add/'

    def form_valid(self, form):
        form.save()

        return super(WordAddView, self).form_valid(form)


class WordListView(ListView):
    template_name = 'word_list.html'
    model = Word

    def get_queryset(self):
        queryset = Word.objects.all()

        return queryset


class WordDeleteView(View):
    def post(self, request, *args, **kwargs):
        word = Word.objects.get(id=self.kwargs['pk'])
        word.delete()
        return JsonResponse({'result': 'True'})


class WordTranslate(View):
    def post(self, request):
        question = request.POST['question']
        client_id = os.getenv('PAPAGO_API_CLIENT_ID')
        client_secret = os.getenv('PAPAGO_API_CLIENT_SECRET')
        if client_id is None or client_secret is None:
            print("Error : Missed Environment Variable")
            return

        encText = urllib.parse.quote(question)
        lang = WordTranslate.what_is_language(question)
        if lang == 'en':
            data = "source=en&target=ko&text=" + encText
        elif lang == 'ko':
            data = "source=ko&target=en&text=" + encText
        else:
            return

        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            response_data = json.loads(response_body)
            translated_text = response_data['message']['result']['translatedText']
            return JsonResponse({'result': translated_text})
        else:
            print("Error Code:" + rescode)

    @staticmethod
    def what_is_language(question):
        import re
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        word = question.split(' ')[0]
        result = hangul.sub('', word)

        if len(result) > 0:
            return 'ko'
        else:
            return 'en'


class WordStudy(View):
    template_name = 'study_word.html'

    def get(self, request):
        word = Word.objects.all().order_by('?').first()

        return render(request, self.template_name, {'word': word})

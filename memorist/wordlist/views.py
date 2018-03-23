import os
import json
import urllib.request

from django.views import View
from django.shortcuts import render
from django.views.generic import *
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from wordlist.forms import WordAddForm
from wordlist.models import Word

from utils.utils import is_sentence


class WordAddView(LoginRequiredMixin, FormView):
    form_class = WordAddForm
    template_name = 'add_word.html'
    success_url = '/words/add/'

    def form_valid(self, form):
        word = form.save(commit=False)
        word.user = self.request.user
        word.save()

        return super(WordAddView, self).form_valid(form)


class WordListView(LoginRequiredMixin, ListView):
    template_name = 'word_list.html'
    model = Word

    def get_queryset(self):
        queryset = Word.alive_objects.filter(user=self.request.user).order_by('-created_time')

        return queryset


class DeletedWordListView(LoginRequiredMixin, ListView):
    template_name = 'deleted_word_list.html'
    model = Word

    def get_queryset(self):
        queryset = Word.objects.filter(user=self.request.user, is_deleted=True).order_by('-modified_time')

        return queryset


class WordDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        word = Word.objects.get(id=self.kwargs['pk'])
        word.is_deleted = True
        word.save()
        return JsonResponse({'result': 'True'})


class WordRestore(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        word = Word.objects.get(id=self.kwargs['pk'])
        word.is_deleted = False
        word.save()
        return JsonResponse({'result': 'True'})


class WordEdit(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        word = Word.objects.get(id=self.kwargs['pk'])
        word.question = self.request.POST['question']
        word.answer = self.request.POST['answer']
        word.save()
        return JsonResponse({'result': 'True'})


class WordTranslate(LoginRequiredMixin, View):
    def post(self, request):
        question = request.POST['question']
        lang = WordTranslate.what_is_language(question)
        translated_result = {}

        papago_translation_result = WordTranslate.request_papago_api(question, lang)
        if papago_translation_result is False:
            print('Error : papago API request fail')

        translated_result['papago_translation_result'] = papago_translation_result

        if not is_sentence(question):
            glosbe_translation_result = WordTranslate.request_glosbe_api(question, lang)
            glosbe_translation_result = WordTranslate.refine_words(glosbe_translation_result)
            if glosbe_translation_result is False:
                print('Error : glosbe API request fail')
            translated_result['glosbe_translation_result'] = glosbe_translation_result

        return JsonResponse(translated_result)

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

    @staticmethod
    def request_papago_api(question, lang):
        client_id = os.getenv('PAPAGO_API_CLIENT_ID')
        client_secret = os.getenv('PAPAGO_API_CLIENT_SECRET')
        if client_id is None or client_secret is None:
            print("Error : Missed Environment Variable")
            return

        text = urllib.parse.quote(question)
        if lang == 'en':
            data = "source=en&target=ko&text=" + text
        elif lang == 'ko':
            data = "source=ko&target=en&text=" + text
        else:
            return

        PAPAGO_URL = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(PAPAGO_URL)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            response_data = json.loads(response_body)
            translated_text = response_data['message']['result']['translatedText']
            return translated_text
        else:
            print("Error Code:" + rescode)
            return False

    @staticmethod
    def request_glosbe_api(question, lang):
        text = urllib.parse.quote(question)
        if lang == 'en':
            data = "from=eng&dest=kor&format=json&pretty=true&phrase=" + text
        elif lang == 'ko':
            data = "from=kor&dest=eng&format=json&pretty=true&phrase=" + text
        else:
            return

        GLOSBE_URL = 'https://glosbe.com/gapi/translate'
        response = urllib.request.urlopen(GLOSBE_URL + '?' + data)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            response_data = json.loads(response_body)
            translated_text = [i.get('phrase')['text'] for i in response_data['tuc'] if i.get('phrase')]
            return translated_text
        else:
            print("Error Code:" + rescode)
            return False

    @staticmethod
    def refine_words(words):
        lowered_words = [word.lower() for word in words]
        result_words = []

        for word in lowered_words:
            if word not in result_words:
                result_words.append(word)

        return result_words


class WordStudy(LoginRequiredMixin, View):
    template_name = 'study_word.html'

    def get(self, request):
        word = Word.alive_objects.filter(user=request.user).order_by('?').first()

        return render(request, self.template_name, {'word': word})


class WordStudyNext(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        question_type = request.POST.get('questionType')
        if question_type == "Words":
            word = Word.alive_objects.filter(user=request.user, question_type='W').order_by('?').first()
        elif question_type == "Sentences":
            word = Word.alive_objects.filter(user=request.user, question_type='S').order_by('?').first()
        else:
            word = Word.alive_objects.filter(user=request.user).order_by('?').first()

        if word is None:
            return JsonResponse({
                'errorType': 'NotExist'
            })
        else:
            return JsonResponse({
                'id': word.id,
                'question': word.question,
                'answer': word.answer,
            })


class MakeTest(LoginRequiredMixin, View):
    def get(self, request):
        num = int(request.GET['num'])
        alive_word_list = Word.alive_objects.filter(user=request.user)
        test_word_list = alive_word_list[len(alive_word_list)-num:]
        json_result = []
        for word in test_word_list:
            json_result.append({
                'question': word.question,
                'answer': word.answer
            })

        return JsonResponse({
            'testWordList': json_result
        })


class Pronounce(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        question = request.POST['question']

        file_name = 'pronounce_' + question[:10] + '.mp3'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        if not os.path.isfile(file_path):
            lang = WordTranslate.what_is_language(question)

            client_id = os.getenv('PAPAGO_API_CLIENT_ID')
            client_secret = os.getenv('PAPAGO_API_CLIENT_SECRET')
            if client_id is None or client_secret is None:
                print("Error : Missed Environment Variable")
                return

            PAPAGO_URL = "https://openapi.naver.com/v1/voice/tts.bin"
            text = urllib.parse.quote(question)

            if lang == 'en':
                data = "speaker=clara&speed=0&text=" + text
            elif lang == 'ko':
                data = "speaker=mijin&speed=0&text=" + text

            else:
                return

            request = urllib.request.Request(PAPAGO_URL)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(request, data=data.encode('utf-8'))
            rescode = response.getcode()

            if rescode == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.read())
            else:
                print("Error Code:" + rescode)
                return False

        return JsonResponse({
            'file_name': file_name,
        })

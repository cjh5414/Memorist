from django.views.generic import FormView, ListView

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

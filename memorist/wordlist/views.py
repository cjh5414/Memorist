from django.views.generic import FormView

from wordlist.forms import WordAddForm


class WordAddView(FormView):
    form_class = WordAddForm
    template_name = 'add_word.html'
    success_url = '/words/add/'

    def form_valid(self, form):
        form.save()

        return super(WordAddView, self).form_valid(form)

from django import forms
from wordlist.models import Word


class WordAddForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['question', 'answer']

        labels = {
            'question': 'Question',
            'answer': 'Answer',
        }

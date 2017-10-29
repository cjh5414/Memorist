import pytest

from wordlist.models import *


@pytest.mark.django_db
def test_add_word(client):
    response = client.get('/words/add/')

    assert 'Question' in response.content.decode('utf-8')
    assert 'Answer' in response.content.decode('utf-8')

    client.post('/words/add/', {
        'question': '노트북',
        'answer': 'laptop',
    })

    word = Word.objects.get(question='노트북')

    assert word.answer == 'laptop'


@pytest.mark.django_db
def test_view_words(client):
    response = client.get('/words/')

    words = Word.objects.all()

    for word in words:
        assert word.question in response.content.decode('utf-8')
        assert word.answer in response.content.decode('utf-8')

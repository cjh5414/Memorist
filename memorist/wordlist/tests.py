import pytest

from wordlist.models import *


@pytest.mark.django_db
def test_add_word(client):
    response = client.get('/words/add/')

    assert 'Question' in response.content.decode('utf-8')
    assert 'Answer' in response.content.decode('utf-8')

    client.post('/words/add/', {
        'question': '사과',
        'answer': 'apple',
    })

    word = Word.objects.get(question='사과')

    assert word.answer == 'apple'


import pytest
import json

from wordlist.models import *
from wordlist.views import WordTranslate

from account.account_tests import testuser_login


@pytest.mark.django_db
def test_add_word(client):
    testuser_login(client)
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
    testuser_login(client)
    response = client.get('/words/')

    words = Word.objects.all()

    for word in words:
        assert word.question in response.content.decode('utf-8')
        assert word.answer in response.content.decode('utf-8')


@pytest.mark.django_db
def test_delete_word(client):
    testuser_login(client)
    word = Word.objects.get(question='사과')

    word_list_response = client.get('/words/')
    assert '사과' in word_list_response.content.decode('utf-8')

    response = client.post('/words/%d/delete/' % word.id)
    assert json.loads(response.content)['result'] == 'True'

    delete_word = Word.objects.get(question='사과')
    assert delete_word.is_deleted is True

    word_list_response = client.get('/words/')
    assert '사과' not in word_list_response.content.decode('utf-8')


@pytest.mark.django_db
def test_translate_api_ko_to_en(client):
    testuser_login(client)
    response = client.post('/translate/', {
        'question': '번역',
    })

    response_data = json.loads(response.content)
    assert response.status_code == 200
    assert response_data['papago_translation_result'] == 'translation'
    assert response_data['glosbe_translation_result'][0] == 'translation'
    assert response_data['glosbe_translation_result'][1] == 'version'

    response = client.post('/translate/', {
        'question': '과일',
    })

    response_data = json.loads(response.content)
    assert response.status_code == 200
    assert response_data['papago_translation_result'] == 'Fruit'
    assert response_data['glosbe_translation_result'][0] == 'fruit'


@pytest.mark.django_db
def test_translate_api_en_to_ko(client):
    testuser_login(client)
    response = client.post('/translate/', {
        'question': 'nurse',
    })

    response_data = json.loads(response.content)
    assert response.status_code == 200
    assert response_data['papago_translation_result'] == '간호사.'
    assert '간호원' in response_data['glosbe_translation_result']
    assert '간호사' in response_data['glosbe_translation_result']

    response = client.post('/translate/', {
        'question': 'i am a boy',
    })

    response_data = json.loads(response.content)
    assert response.status_code == 200
    assert response_data['papago_translation_result'] == '나는 소년 입니다.'
    assert 'glosbe_translation_result' not in response_data


@pytest.mark.django_db
def test_basic_study_view(client):
    testuser_login(client)
    response = client.get('/study/')

    assert '다음' in response.content.decode('utf-8')
    assert '답 확인' in response.content.decode('utf-8')
    assert '제거' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_study_api(client):
    testuser_login(client)
    response = client.post('/study/next/')

    response_data = json.loads(response.content)

    assert response.status_code == 200
    word = Word.objects.get(question=response_data['question'])
    assert word.answer == response_data['answer']


@pytest.mark.django_db
def test_confirm_deleted_word(client):
    testuser_login(client)
    word = Word.objects.get(question='사과')

    response = client.get('/words/deleted/')
    assert word.question not in response.content.decode('utf-8')

    client.post('/words/%d/delete/' % word.id)

    response = client.get('/words/deleted/')
    assert word.question in response.content.decode('utf-8')


@pytest.mark.django_db
def test_restore_deleted_word(client):
    testuser_login(client)
    word = Word.objects.get(question='사과')

    client.post('/words/%d/delete/' % word.id)

    word = Word.objects.get(question='사과')
    assert word.is_deleted is True

    client.post('/words/%d/restore/' % word.id)

    word = Word.objects.get(question='사과')
    assert word.is_deleted is False


@pytest.mark.django_db
def test_refine_words(client):
    testuser_login(client)
    words = ['apple', 'apple', 'Cup', 'cup', 'shorts', 'Hat']

    result_words = WordTranslate.refine_words(words)

    assert result_words == ['apple', 'cup', 'shorts', 'hat']

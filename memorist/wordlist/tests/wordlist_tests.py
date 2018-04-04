import pytest
import json
import os

from django.conf import settings

from wordlist.models import *
from account.models import User

from wordlist.views import WordTranslate

from account.account_tests import testuser_login


@pytest.mark.django_db
def test_add_word(client):
    testuser_login(client, 'test2')
    response = client.get('/words/add/')

    assert 'Question' in response.content.decode('utf-8')
    assert 'Answer' in response.content.decode('utf-8')

    client.post('/words/add/', {
        'question': '노트북',
        'answer': 'laptop',
    })

    word = Word.objects.get(question='노트북')

    assert word.answer == 'laptop'
    assert word.user.username == 'test2'


@pytest.mark.django_db
def test_edit_word(client):
    testuser_login(client, 'test2')

    client.post('/words/add/', {
        'question': 'sarcastic',
        'answer': '비고는',
    })

    word = Word.objects.get(question='sarcastic', answer='비고는')

    response = client.post('/words/%d/edit/' % word.id, {
        'question': 'sarcastic',
        'answer': '비꼬는',
    })

    assert response.status_code == 200

    edited_word = Word.objects.get(id=word.id)

    assert edited_word.answer == '비꼬는'


@pytest.mark.django_db
def test_distinguish_question_type_when_adding(client):
    testuser_login(client, 'test2')

    client.post('/words/add/', {
        'question': '단어',
        'answer': 'word',
    })

    word = Word.objects.get(question='단어', answer='word')
    assert word.question_type == 'W'

    client.post('/words/add/', {
        'question': '이것은 문장입니다.',
        'answer': 'This is a sentence.',
    })

    word = Word.objects.get(question='이것은 문장입니다.', answer='This is a sentence.')
    assert word.question_type == 'S'


@pytest.mark.django_db
def test_view_words(client):
    testuser_login(client)
    response = client.get('/words/')

    owner = User.objects.get(username='test')
    words = Word.alive_objects.filter(user=owner)

    for word in words:
        assert word.question in response.content.decode('utf-8')
        assert word.answer in response.content.decode('utf-8')


@pytest.mark.django_db
def test_show_only_own_words(client):
    testuser_login(client)
    response = client.get('/words/')

    owner = User.objects.get(username='test')
    another = User.objects.get(username='test2')

    for word in Word.alive_objects.filter(user=owner):
        assert word.question in response.content.decode('utf-8')

    for word in Word.alive_objects.filter(user=another):
        assert word.question not in response.content.decode('utf-8')


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
def test_en_en_dictionary_api(client):
    testuser_login(client)

    response = client.post('/translate/', {
        'question': 'ace',
    })

    response_data = json.loads(response.content)
    assert response_data['oxford_dictionary_result'][0]['definitions'][0] == \
           'a playing card with a single spot on it, ranked as the highest card in its suit in most card games'

    assert response_data['oxford_dictionary_result'][0]['examples'][0] == \
           'the ace of diamonds'

    assert response_data['oxford_dictionary_result'][1]['definitions'][0] == \
           'a person who excels at a particular sport or other activity'

    assert response_data['oxford_dictionary_result'][1]['examples'][0] == \
           'a motorcycle ace'


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
def test_show_only_own_deleted_words(client):
    testuser_login(client)

    word = Word.objects.get(question='사과')
    client.post('/words/%d/delete/' % word.id)

    response = client.get('/words/deleted/')

    owner = User.objects.get(username='test')
    another = User.objects.get(username='test2')

    for word in Word.objects.filter(user=owner, is_deleted=True):
        assert word.question in response.content.decode('utf-8')

    for word in Word.objects.filter(user=another, is_deleted=True):
        assert word.question not in response.content.decode('utf-8')


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


@pytest.mark.django_db
def test_prounce(client):
    testuser_login(client)

    question = 'i am a boy'
    response = client.post('/pronounce/', {
        'question': question,
    })

    response_data = json.loads(response.content)

    assert response.status_code == 200

    file_name = 'pronounce_' + question + '.mp3'
    assert response_data['file_name'] == file_name
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    assert os.path.isfile(file_path) is True


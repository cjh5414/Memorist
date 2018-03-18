import pytest
import json

from wordlist.models import *

from account.account_tests import testuser_login


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
    assert word.id == response_data['id']


@pytest.mark.django_db
def test_study_view_from_only_own_word_list(client):
    testuser_login(client)

    another = User.objects.get(username='test2')
    words = Word.alive_objects.filter(user=another)
    for i in range(20):
        for word in words:
            response = client.get('/study/')
            assert word.question not in response.content.decode('utf-8')


@pytest.mark.django_db
def test_study_api_from_only_own_word_list(client):
    testuser_login(client)

    another = User.objects.get(username='test2')
    words = Word.alive_objects.filter(user=another)
    for i in range(20):
        for word in words:
            response = client.post('/study/next/')
            response_data = json.loads(response.content)
            assert word.question != response_data['answer']


@pytest.mark.django_db
def test_study_only_words(client):
    testuser_login(client, 'test2')

    def is_sentence(question):
        words = question.split(' ')
        if len(words) > 1:
            return True
        else:
            return False

    for i in range(20):
        response = client.post('/study/next/', {
            'questionType': 'Words'
        })
        response_data = json.loads(response.content)
        assert is_sentence(response_data['question']) is False


@pytest.mark.django_db
def test_study_only_sentences(client):
    testuser_login(client, 'test2')

    def is_sentence(question):
        words = question.split(' ')
        if len(words) > 1:
            return True
        else:
            return False

    for i in range(20):
        response = client.post('/study/next/', {
            'questionType': 'Sentences'
        })
        response_data = json.loads(response.content)
        assert is_sentence(response_data['question']) is True


@pytest.mark.django_db
def test_check_error_when_there_are_only_words(client):
    testuser_login(client)

    response = client.post('/study/next/', {
        'questionType': 'Sentences'
    })

    response_data = json.loads(response.content)
    assert response_data['errorType'] == 'NotExist'

    testuser_login(client, 'test2')

    response = client.post('/study/next/', {
        'questionType': 'Sentences'
    })

    response_data = json.loads(response.content)
    assert 'errorType' not in response_data

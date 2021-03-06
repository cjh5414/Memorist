import pytest
import json
from datetime import timedelta

from wordlist.models import *

from account.account_tests import testuser_login

from utils.utils import is_sentence


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
    response = client.get('/study/next/')

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
            response = client.get('/study/next/')
            response_data = json.loads(response.content)
            assert word.question != response_data['answer']


@pytest.mark.django_db
def test_study_only_words(client):
    user = testuser_login(client, 'test2')
    user.studystatus.question_type = 'W'
    user.save()

    for i in range(20):
        response = client.get('/study/next/')
        response_data = json.loads(response.content)
        assert is_sentence(response_data['question']) is False


@pytest.mark.django_db
def test_study_only_sentences(client):
    user = testuser_login(client, 'test2')
    user.studystatus.question_type = 'S'
    user.save()

    for i in range(20):
        response = client.get('/study/next/')
        response_data = json.loads(response.content)
        assert is_sentence(response_data['question']) is True


@pytest.mark.django_db
def test_study_words_chosen_by_days(client):
    test_user = testuser_login(client, 'empty_words_test')

    words = []
    words.append(Word.objects.create(question='오늘 단어', answer="today's word", user_id=test_user.id))
    words.append(Word.objects.create(question='1일 전 단어', answer='words a day ago', user_id=test_user.id))
    words.append(Word.objects.create(question='2일 전 단어', answer='words two days ago', user_id=test_user.id))
    words.append(Word.objects.create(question='3일 전 단어', answer='words tree days ago', user_id=test_user.id))

    for idx, word in enumerate(words):
        word.created_time = word.created_time - timedelta(days=idx)
        word.save()

    for i in range(4):
        test_user.studystatus.chosen_days = i
        test_user.save()
        response = client.get('/study/next/')

        response_data = json.loads(response.content)
        chosen_questions = [word.question for word in words[:(i+1)]]
        assert response_data['question'] in chosen_questions


@pytest.mark.django_db
def test_if_there_is_no_word_in_chosen_period(client):
    test_user = testuser_login(client, 'empty_words_test')

    word = Word.objects.create(question='오늘 단어', answer="today's word", user_id=test_user.id)
    word.created_time = word.created_time - timedelta(days=3)
    word.save()

    test_user.studystatus.chosen_days = 1
    test_user.save()
    response = client.get('/study/next/')

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data['errorType'] == 'NotExist'


@pytest.mark.django_db
def test_check_error_when_there_are_only_words(client):
    user = testuser_login(client)
    user.studystatus.question_type = 'S'
    user.save()
    response = client.get('/study/next/')

    response_data = json.loads(response.content)
    assert response_data['errorType'] == 'NotExist'

    user2 = testuser_login(client, 'test2')
    user2.studystatus.question_type = 'S'
    user2.save()
    response = client.get('/study/next/')

    response_data = json.loads(response.content)
    assert 'errorType' not in response_data


@pytest.mark.django_db
def test_make_a_test_according_to_number(client):
    testuser_login(client, 'test2')

    for i in range(1, 11):
        client.post('/words/add/', {
            'question': '단어' + str(i),
            'answer': 'word' + str(i),
        })

    response = client.get('/study/test/?num=4')
    response_data = json.loads(response.content)
    test_word_list = response_data['testWordList']

    assert len(test_word_list) == 4
    question_list = []
    for i in range(7, 11):
        question_list.append('단어' + str(i))

    for word in test_word_list:
        assert word['question'] in question_list

    test_question_list = []
    for word in test_word_list:
        test_question_list.append(word['question'])

    assert len(set(test_question_list)) == len(test_question_list)

    response = client.get('/study/test/?num=7')
    response_data = json.loads(response.content)
    test_word_list = response_data['testWordList']

    assert len(test_word_list) == 7
    question_list = []
    for i in range(4, 11):
        question_list.append('단어' + str(i))

    for word in test_word_list:
        assert word['question'] in question_list

    test_question_list = []
    for word in test_word_list:
        test_question_list.append(word['question'])

    assert len(set(test_question_list)) == len(test_question_list)


@pytest.mark.django_db
def test_random_order_in_making_a_test(client):
    testuser_login(client, 'test2')
    ordered_word_list = []

    for i in range(1, 5):
        client.post('/words/add/', {
            'question': '단어' + str(i),
            'answer': 'word' + str(i),
        })

        ordered_word_list.append({
            'question': '단어' + str(i),
            'answer': 'word' + str(i),
        })

    response = client.get('/study/test/?num=4')
    response_data = json.loads(response.content)
    test_word_list = response_data['testWordList']

    assert ordered_word_list != test_word_list


@pytest.mark.django_db
def test_pick_all_of_word_when_making_a_test(client):
    testuser_login(client, 'test2')

    response = client.get('/study/test/?num=All')
    response_data = json.loads(response.content)
    test_word_list = response_data['testWordList']

    words = Word.alive_objects.filter(user__username='test2')

    assert len(test_word_list) == len(words)

    test_question_list = []
    for test_word in test_word_list:
        test_question_list.append(test_word['question'])
    for word in words:
        assert word.question in test_question_list


@pytest.mark.django_db
def test_make_a_test_when_studystatus_are_chosen(client):
    user = testuser_login(client, 'test2')
    user.studystatus.question_type = 'W'
    user.save()

    response = client.get('/study/test/?num=All')
    response_data = json.loads(response.content)
    test_word_list = response_data['testWordList']

    words = Word.alive_objects.filter(user__username='test2').filter(question_type='W')

    assert len(test_word_list) == len(words)

    test_question_list = []
    for test_word in test_word_list:
        test_question_list.append(test_word['question'])
    for word in words:
        assert word.question in test_question_list

    user.studystatus.question_type = 'S'
    user.save()
    response = client.get('/study/test/?num=1')
    response_data = json.loads(response.content)
    test_word_list = response_data['testWordList']

    word = Word.alive_objects.filter(user__username='test2').filter(question_type='S').order_by('created_time').last()

    assert len(test_word_list) == 1
    assert word.question == test_word_list[0]['question']


@pytest.mark.django_db
def test_get_number_of_words_when_status_of_study_is_changed(client):
    user = testuser_login(client, 'test2')
    user.studystatus.question_type = 'S'
    user.studystatus.chosen_days = user.studystatus.ALL_DAYS
    user.save()

    response = client.get('/study/numberofwords/')
    response_data = json.loads(response.content)
    assert response_data['numberOfWords'] == 2

    user.studystatus.question_type = 'W'
    user.save()

    response = client.get('/study/numberofwords/')
    response_data = json.loads(response.content)
    assert response_data['numberOfWords'] == 2

    user.studystatus.question_type = 'A'
    user.studystatus.chosen_days = 1
    user.save()

    response = client.get('/study/numberofwords/')
    response_data = json.loads(response.content)
    assert response_data['numberOfWords'] == 4


@pytest.mark.django_db
def test_get_progress_of_study(client):
    user = testuser_login(client, 'test2')

    total_words_num = Word.objects.filter(user=user).count()
    remained_words_num = Word.alive_objects.filter(user=user).count()

    response = client.get('/study/progress/')
    response_data = json.loads(response.content)
    assert response_data['totalNumberOfWords'] == total_words_num
    assert response_data['studiedNumberOfWords'] == total_words_num - remained_words_num

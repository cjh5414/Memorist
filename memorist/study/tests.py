import pytest
import json

from study.models import Study
from account.models import User
from account.account_tests import testuser_login


@pytest.mark.django_db
def test_create_study_when_account_is_created(client):
    client.post('/signup/', {
        'username': 'studytest',
        'name': 'kimstudy',
        'email': 'kim1923@gmail.com',
        'password1': 'kim1234',
        'password2': 'kim1234',
    })

    study = Study.objects.get(user__username='studytest')
    assert study.chosen_days == study.ALL_DAYS
    assert study.question_type == 'A'


@pytest.mark.django_db
def test_change_question_type(client):
    testuser_login(client)

    user = User.objects.get(username='test')
    assert user.study.question_type == 'A'

    response = client.post('/accounts/study/question-type-change/', {
        'question_type': 'S'
    })

    response_data = json.loads(response.content)
    assert response_data['result'] == 'Success'

    user = User.objects.get(username='test')
    assert user.study.question_type == 'S'


@pytest.mark.django_db
def test_change_chosen_days(client):
    testuser_login(client)

    user = User.objects.get(username='test')
    assert user.study.chosen_days == Study.ALL_DAYS

    response = client.post('/accounts/study/chosen-days-change/', {
        'chosen_days': 30,
    })

    response_data = json.loads(response.content)
    assert response_data['result'] == 'Success'

    user = User.objects.get(username='test')
    assert user.study.chosen_days == 30

    response = client.post('/accounts/study/chosen-days-change/', {
        'chosen_days': -1,
    })

    response_data = json.loads(response.content)
    assert response_data['result'] == 'Success'

    user = User.objects.get(username='test')
    assert user.study.chosen_days == -1

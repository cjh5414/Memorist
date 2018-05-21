import pytest
import json

from studystatus.models import StudyStatus
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

    studystatus = StudyStatus.objects.get(user__username='studytest')
    assert studystatus.chosen_days == studystatus.ALL_DAYS
    assert studystatus.question_type == 'A'


@pytest.mark.django_db
def test_update_study_when_account_is_updated(client):
    user = User.objects.get(username="test")
    studystatus = StudyStatus.objects.get(user__username="test")

    assert studystatus.chosen_days == studystatus.ALL_DAYS
    assert studystatus.question_type == 'A'

    user.studystatus.chosen_days = 20
    user.studystatus.question_type = 'S'
    user.save()

    changed_study = StudyStatus.objects.get(user__username="test")

    assert changed_study.chosen_days == 20
    assert changed_study.question_type == 'S'


@pytest.mark.django_db
def test_change_question_type(client):
    user = testuser_login(client)
    assert user.studystatus.question_type == 'A'

    response = client.post('/accounts/studystatus/question-type-change/', {
        'question_type': 'S'
    })

    response_data = json.loads(response.content)
    assert response_data['result'] == 'Success'

    user = User.objects.get(username='test')
    assert user.studystatus.question_type == 'S'


@pytest.mark.django_db
def test_change_chosen_days(client):
    user = testuser_login(client)
    assert user.studystatus.chosen_days == StudyStatus.ALL_DAYS

    response = client.post('/accounts/studystatus/chosen-days-change/', {
        'chosen_days': 30,
    })

    response_data = json.loads(response.content)
    assert response_data['result'] == 'Success'

    user = User.objects.get(username='test')
    assert user.studystatus.chosen_days == 30

    response = client.post('/accounts/studystatus/chosen-days-change/', {
        'chosen_days': -1,
    })

    response_data = json.loads(response.content)
    assert response_data['result'] == 'Success'

    user = User.objects.get(username='test')
    assert user.studystatus.chosen_days == -1


@pytest.mark.django_db
def test_get_studystatus(client):
    user = testuser_login(client)

    response = client.get('/accounts/studystatus/')
    response_data = json.loads(response.content)

    assert response_data['question_type'] == 'A'
    assert response_data['chosen_days'] == -1

    user.studystatus.question_type = 'S'
    user.studystatus.chosen_days = 15
    user.save()

    response = client.get('/accounts/studystatus/')
    response_data = json.loads(response.content)

    assert response_data['question_type'] == 'S'
    assert response_data['chosen_days'] == 15

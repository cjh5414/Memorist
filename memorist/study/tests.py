import pytest
from study.models import Study


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

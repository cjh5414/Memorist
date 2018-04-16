import pytest
from account.models import User


@pytest.mark.django_db
def testuser_login(client, username='test'):
    client.post('/login/', {'username': username, 'password': 'test1234!'})


@pytest.mark.django_db
def test_signup(client):
    response = client.get('/signup/')
    assert 'Sign Up' in response.content.decode('utf-8')
    assert 'ID' in response.content.decode('utf-8')
    assert 'EMAIL' in response.content.decode('utf-8')
    assert 'PASSWORD' in response.content.decode('utf-8')
    assert 'CONFIRM PASSWORD' in response.content.decode('utf-8')

    response = client.post('/signup/', {
        'username': 'memo1920',
        'email': 'memo1920@gmail.com',
        'password1': 'mm1234!',
        'password2': 'mm1234!',
    })

    assert response.status_code == 302
    assert response.url == '/login/'

    user = User.objects.get(username='memo1920')
    assert user.email == 'memo1920@gmail.com'


@pytest.mark.django_db
def test_login(client):
    response = client.get('/login/')
    assert 'Sign In' in response.content.decode('utf-8')
    assert 'ID' in response.content.decode('utf-8')
    assert 'PASSWORD' in response.content.decode('utf-8')

    response = client.post('/login/', {'username': 'test', 'password': 'test1234!'})
    assert response.url == '/words/add/'


@pytest.mark.django_db
def test_have_to_login_before_do_everything(client):
    response = client.get('/words/add/')
    assert response.status_code == 302
    assert response.url == '/login/?next=/words/add/'

    testuser_login(client)
    response = client.get('/words/add/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_have_to_login_if_call_api(client):
    response = client.post('/translate/', {
        'question': '번역',
    })
    assert response.status_code == 302
    assert response.url == '/login/?next=/translate/'

    testuser_login(client)
    response = client.post('/translate/', {
        'question': '번역',
    })

    assert response.status_code == 200



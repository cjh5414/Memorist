import pytest


@pytest.mark.django_db
def testuser_login(client):
    client.post('/login/', {'username': 'test', 'password': 'test1234!'})


@pytest.mark.django_db
def test_login(client):
    response = client.get('/login/')
    assert '로그인' in response.content.decode('utf-8')
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


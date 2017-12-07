import pytest

from account.models import User


@pytest.mark.django_db
def test_signup(client):
    response = client.get('/login/')
    assert '로그인' in response.content.decode('utf-8')
    assert 'ID' in response.content.decode('utf-8')
    assert 'PASSWORD' in response.content.decode('utf-8')

    response = client.post('/login/', {'username': 'test', 'password': 'test1234!'})
    assert response.url == '/words/add/'

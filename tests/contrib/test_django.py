import pytest
from polls.models import Question


@pytest.mark.urls('urlconf_dispatch_request')
def test_dispatch_request(client):
    """Dispatch request to the `Injector` subclass attributes."""

    response = client.get('/comments/1/test/')
    assert response.status_code == 200
    assert response.content == b'<h1>OK</h1>'


@pytest.mark.urls('urlconf_inject_user')
def test_inject_user(client):
    """Access request user property."""

    response = client.get('/comments/1/test/')
    assert response.status_code == 200
    assert response.content == b'<h1>OK</h1>'


@pytest.mark.urls('urlconf_pass_kwargs_to_the_service')
def test_pass_kwargs_to_the_service(client):
    """Pass kwargs to the nested service object."""

    response = client.get('/comments/1/test/')
    assert response.status_code == 200
    assert response.content == b'<h1>OK</h1>'


@pytest.mark.django_db
@pytest.mark.urls('urlconf_create_view')
def test_create_view(client):
    """Define injectable create view."""

    response = client.get('/polls/add/')
    assert response.status_code == 200

    response = client.post(
        '/polls/add/',
        {
            'question_text': 'foo',
            'pub_date': '2018-02-05 00:37:50',
        },
        follow=True,
    )
    assert response.status_code == 200
    assert Question.objects.filter(question_text='foo').exists()

import pytest


@pytest.mark.urls('urlconf_dispatch_request')
def test_dispatch_request(client):
    """Dispatch request to the `Injector` subclass attributes."""

    response = client.get('/comments/1/test/')
    assert response.status_code == 200
    assert response.content == b'<h1>OK</h1>'

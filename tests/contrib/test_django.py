def test_dispatch_request(client):
    """Dispatch request to the `Injector` subclass attributes."""

    response = client.get("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


def test_inject_user(client):
    """Access request user property."""

    response = client.get("/test_inject_user/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


def test_pass_kwargs(client):
    """Pass kwargs to the nested service object."""

    response = client.get("/test_pass_kwargs/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"

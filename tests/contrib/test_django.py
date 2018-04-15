def test_dispatch_request(client):
    """Dispatch request to the `Injector` subclass attributes."""

    response = client.get("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"

    response = client.post("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"

    response = client.put("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"

    response = client.patch("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"

    response = client.delete("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"

    response = client.head("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b""

    response = client.options("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"

    response = client.trace("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


def test_empty_request(client):
    """
    Use method not allowed, if `Injector` subclass doesn't define an
    attribute for this method.
    """

    response = client.get("/test_empty_request/1/test/")
    assert response.status_code == 405

    response = client.post("/test_empty_request/1/test/")
    assert response.status_code == 405

    response = client.put("/test_empty_request/1/test/")
    assert response.status_code == 405

    response = client.patch("/test_empty_request/1/test/")
    assert response.status_code == 405

    response = client.delete("/test_empty_request/1/test/")
    assert response.status_code == 405

    response = client.head("/test_empty_request/1/test/")
    assert response.status_code == 405

    response = client.trace("/test_empty_request/1/test/")
    assert response.status_code == 405


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

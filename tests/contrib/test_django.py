import pytest
from dependencies import Injector
from dependencies.contrib.django import form_view, view
from django.views.generic import View


@pytest.mark.parametrize("method", set(View.http_method_names) - {"head"})
def test_dispatch_request(client, method):
    """Dispatch request to the `Injector` subclass attributes."""

    response = getattr(client, method)("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


@pytest.mark.parametrize("method", set(View.http_method_names) - {"options"})
def test_empty_request(client, method):
    """
    Use method not allowed, if `Injector` subclass doesn't define an
    attribute for this method.
    """

    response = getattr(client, method)("/test_empty_request/1/test/")
    assert response.status_code == 405


@pytest.mark.parametrize("method", set(View.http_method_names) - {"head"})
def test_inject_user(client, method):
    """Access request user property."""

    response = getattr(client, method)("/test_inject_user/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


@pytest.mark.parametrize("method", set(View.http_method_names) - {"head"})
def test_inject_kwargs(client, method):
    """Pass kwargs to the nested service object."""

    response = getattr(client, method)("/test_inject_kwargs/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


@pytest.mark.parametrize("method", set(View.http_method_names) - {"head"})
def test_inject_self(client, method):
    """Access generated view instance."""

    response = getattr(client, method)("/test_inject_self/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


def test_form_view(client):
    """Retrieve and submit form view created from injector."""

    response = client.get("/test_form_view/")
    assert response.status_code == 200

    response = client.post(
        "/test_form_view/", {"question_text": "foo", "pub_date": "12/23/2008 00:12"}
    )
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"

    response = client.post("/test_form_view/", {"question_text": "foo"})
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


def test_docstring():
    """Access `view` docstring."""

    assert view.__doc__ == "Create Django class-based view from injector class."
    assert (
        form_view.__doc__
        == "Create Django form processing class-based view from injector class."
    )

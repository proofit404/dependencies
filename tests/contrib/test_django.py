import django
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
    if django.VERSION >= (2, 0):
        assert response.content == b"extra-var"

    response = client.post(
        "/test_form_view/",
        {"test-question_text": "foo", "test-pub_date": "12/23/2008 00:12"},
    )
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"

    response = client.post("/test_form_view/", {"bad": "input"})
    assert response.status_code == 200
    assert response.content == b"<h1>ERROR</h1>"


def test_form_view_attributes():
    """Access attributes of generated FormView."""

    from polls.views import QuestionFormView

    view_class = QuestionFormView.as_view().view_class
    assert view_class.template_name == "question.html"
    assert view_class.template_engine == "default"
    assert view_class.response_class.__name__ == "TestTemplateResponse"
    assert view_class.content_type == "text/html"
    assert view_class.initial == {"is_testing": True}


def test_docstrings():
    """Access `view` and `form_view` docstring."""

    assert view.__doc__ == "Create Django class-based view from injector class."
    assert (
        form_view.__doc__
        == "Create Django form processing class-based view from injector class."
    )

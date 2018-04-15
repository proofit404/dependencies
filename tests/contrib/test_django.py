import pytest
from dependencies import Injector
from dependencies.contrib.django import view
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


def test_override_method_names(client):
    """Define http method names in the generated `Handler`."""

    @view
    class ContainerView(Injector):

        get = lambda: None
        post = lambda: None
        head = lambda: None

    viewfunc = ContainerView.as_view()

    assert viewfunc.view_class.http_method_names == ["head", "options", "get", "post"]

import pytest

from dependencies.exceptions import DependencyError

django = pytest.importorskip("django")
generic_views = pytest.importorskip("django.views.generic")
contrib = pytest.importorskip("dependencies.contrib.django")


http_methods = set(generic_views.View.http_method_names)
http_methods_no_head = http_methods - {"head"}
http_methods_no_options = http_methods - {"options"}
http_methods_safe = {"get", "head", "options"}


# View.


@pytest.mark.parametrize("method", http_methods_no_head)
def test_dispatch_request(client, method):
    """Dispatch request to the `Injector` subclass attributes."""

    response = getattr(client, method)("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


@pytest.mark.parametrize("method", http_methods_no_options)
def test_empty_request(client, method):
    """
    Use method not allowed, if `Injector` subclass doesn't define an
    attribute for this method.
    """

    response = getattr(client, method)("/test_empty_request/1/test/")
    assert response.status_code == 405


@pytest.mark.parametrize("method", http_methods_no_head)
def test_inject_user(client, method):
    """Access request user property."""

    response = getattr(client, method)("/test_inject_user/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


@pytest.mark.parametrize("method", http_methods_no_head)
def test_inject_kwargs(client, method):
    """Pass kwargs to the nested service object."""

    response = getattr(client, method)("/test_inject_kwargs/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


@pytest.mark.parametrize("method", http_methods_no_head)
def test_inject_self(client, method):
    """Access generated view instance."""

    response = getattr(client, method)("/test_inject_self/1/test/")
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"


# Template view.


@pytest.mark.parametrize("url", ["test_template_view", "test_template_view_dynamic"])
def test_template_view(client, url):
    """Retrieve template view created from injector."""

    response = client.get("/%s/1/" % (url,))
    assert response.status_code == 200
    if django.VERSION >= (2, 0):
        assert response.content == b"extra-var\n"


def test_template_view_attributes():
    """Access attributes of generated TemplateView."""

    from django_project.views import QuestionTemplateView

    view = QuestionTemplateView.as_view().view_class()
    assert view.template_name == "question.html"
    assert view.template_engine == "default"
    assert view.response_class.__name__ == "TestTemplateResponse"
    assert view.content_type == "text/html"


# Form view.


# FIXME: Support dynamic fields.
def test_form_view(client):
    """Retrieve and submit form view created from injector."""

    response = client.get("/test_form_view/1/")
    assert response.status_code == 200
    if django.VERSION >= (2, 0):
        assert response.content == b"extra-var\n"

    response = client.post(
        "/test_form_view/1/",
        {"test-question_text": "foo", "test-pub_date": "12/23/2008 00:12"},
    )
    assert response.status_code == 200
    assert response.content == b"<h1>OK</h1>"

    response = client.post("/test_form_view/1/", {"bad": "input"})
    assert response.status_code == 200
    assert response.content == b"<h1>ERROR</h1>"


def test_form_view_undefined_method(client):
    """
    Throw error if corresponding form view method is not defined in
    the injector.
    """

    with pytest.raises(DependencyError) as exc_info:
        client.post(
            "/empty_form_view/",
            {"question_text": "foo", "pub_date": "12/23/2008 00:12"},
        )
    message = str(exc_info.value)
    assert message == "Add 'form_valid' to the 'EmptyFormView' injector"

    with pytest.raises(DependencyError) as exc_info:
        client.post("/empty_form_view/")
    message = str(exc_info.value)
    assert message == "Add 'form_invalid' to the 'EmptyFormView' injector"


def test_form_view_attributes():
    """Access attributes of generated FormView."""

    from django_project.views import QuestionFormView

    view = QuestionFormView.as_view().view_class()
    assert view.success_url == "/thanks/"
    assert view.template_name == "question.html"
    assert view.template_engine == "default"
    assert view.response_class.__name__ == "TestTemplateResponse"
    assert view.content_type == "text/html"
    assert view.initial == {"is_testing": True}


# Attributes.


def test_docstrings():
    """Access `view` and `form_view` docstring."""

    assert contrib.view.__doc__ == "Create Django class-based view from injector class."
    assert (
        contrib.template_view.__doc__
        == "Create Django template class-based view from injector class."
    )
    assert (
        contrib.form_view.__doc__
        == "Create Django form processing class-based view from injector class."
    )


def test_keep_view_informanion():
    """Generated view should point to the `Injector` subclass."""

    from django_project.views import (
        DispatchView,
        QuestionTemplateView,
        QuestionFormView,
    )

    view = DispatchView.as_view()

    assert view.__name__ == "DispatchView"
    assert view.__module__ == "django_project.views"
    assert view.__doc__ == "Intentionally left blank."

    template_view = QuestionTemplateView.as_view()

    assert template_view.__name__ == "QuestionTemplateView"
    assert template_view.__module__ == "django_project.views"
    assert template_view.__doc__ == "Intentionally left blank."

    form_view = QuestionFormView.as_view()

    assert form_view.__name__ == "QuestionFormView"
    assert form_view.__module__ == "django_project.views"
    assert form_view.__doc__ == "Intentionally left blank."

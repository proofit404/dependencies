import pytest

from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError

admin_models = pytest.importorskip("django.contrib.admin.models")
auth_models = pytest.importorskip("django.contrib.auth.models")
status = pytest.importorskip("rest_framework.status")
test_client = pytest.importorskip("rest_framework.test")
contrib = pytest.importorskip("dependencies.contrib.rest_framework")
project_exceptions = pytest.importorskip("django_project.api.exceptions")
project_commands = pytest.importorskip("django_project.api.commands")
project_throttle = pytest.importorskip("django_project.api.throttle")


client = test_client.APIClient()


def test_dispatch_request(db):
    """
    Dispatch request to the `Injector` subclass attributes.

    DRF APIView render, parser, permissions and other attributes
    should be respected.
    """

    response = client.post("/api/action/", {"last": True}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.content.decode().lstrip().startswith("<!DOCTYPE html>")

    # Parser classes mismatch.

    response = client.post("/api/action/", {"last": True})
    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    # Permission classes applies.

    response = client.get("/api/login/")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Authentication classes applies.

    auth_models.User.objects.create(
        pk=1, username="johndoe", first_name="John", last_name="Doe"
    )

    response = client.get("/api/login_all/")
    assert response.status_code == status.HTTP_200_OK

    # Throttle classes applies.

    response = client.get("/api/throttle_all/")
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    # Strict content negotiation.

    with pytest.raises(project_exceptions.NegotiationError):
        client.get("/api/negotiate/")

    # Versioning classes applies.

    with pytest.raises(project_exceptions.VersionError):
        client.get("/api/versioning/")

    # Metadata classes applies.

    with pytest.raises(project_exceptions.MetadataError):
        client.options("/api/metadata/")


def test_dispatch_request_generic_view_retrieve(db):
    """
    Retrieve user details through view defined with injector subclass.
    """

    auth_models.User.objects.create(
        pk=1, username="johndoe", first_name="John", last_name="Doe"
    )

    response = client.get("/api/users/johndoe/", format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
    }


@pytest.mark.parametrize("basename", ["users", "user_fields"])
def test_dispatch_request_generic_view_list(db, basename):
    """
    List user details through view defined with injector subclass.
    """

    auth_models.User.objects.create(
        pk=1, username="johndoe", first_name="John", last_name="Doe"
    )
    auth_models.User.objects.create(
        pk=2, username="foo", first_name="bar", last_name="baz"
    )

    response = client.get(
        "/api/%s/?username=johndoe&limit=1" % (basename,), format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {"id": 1, "username": "johndoe", "first_name": "John", "last_name": "Doe"}
        ],
    }


@pytest.mark.parametrize("basename", ["user_set", "dynamic_user_set"])
def test_dispatch_request_model_view_set(db, basename):
    """
    List, retrieve, create, update & delete actions in the
    `ModelViewSet` defined with `Injector` subclass.
    """

    auth_models.User.objects.create(
        pk=1, username="admin", first_name="admin", last_name="admin"
    )

    response = client.post(
        "/api/%s/" % (basename,),
        {"username": "johndoe", "first_name": "John", "last_name": "Doe"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
    }
    assert admin_models.LogEntry.objects.filter(
        action_flag=admin_models.ADDITION
    ).exists()

    response = client.get("/api/%s/" % (basename,))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 2, "username": "johndoe", "first_name": "John", "last_name": "Doe"}
    ]

    response = client.get("/api/%s/2/" % (basename,))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
    }

    response = client.put(
        "/api/%s/2/" % (basename,), {"username": "johndoe", "first_name": "Jim"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "Jim",
        "last_name": "Doe",
    }
    assert admin_models.LogEntry.objects.filter(
        action_flag=admin_models.CHANGE
    ).exists()

    response = client.patch("/api/%s/2/" % (basename,), {"last_name": "Worm"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "Jim",
        "last_name": "Worm",
    }
    assert (
        admin_models.LogEntry.objects.filter(action_flag=admin_models.CHANGE).count()
        == 2
    )

    response = client.delete("/api/%s/2/" % (basename,))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert admin_models.LogEntry.objects.filter(
        action_flag=admin_models.DELETION
    ).exists()


def test_model_view_set_undefined_method(db):
    """
    Throw error if corresponding model view set action method is not
    defined in the injector.
    """

    auth_models.User.objects.create(
        pk=1, username="admin", first_name="admin", last_name="admin"
    )

    response = client.get("/api/empty_set/1/")
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/api/empty_set/")
    assert response.status_code == status.HTTP_200_OK

    with pytest.raises(DependencyError) as exc_info:
        client.post("/api/empty_set/", {"username": "johndoe"})
    message = str(exc_info.value)
    assert message == "Add 'create' to the 'EmptyViewSet' injector"

    with pytest.raises(DependencyError) as exc_info:
        client.patch("/api/empty_set/1/", {"username": "jimworm"})
    message = str(exc_info.value)
    assert message == "Add 'update' to the 'EmptyViewSet' injector"

    with pytest.raises(DependencyError) as exc_info:
        client.put("/api/empty_set/1/", {"username": "jimworm"})
    message = str(exc_info.value)
    assert message == "Add 'update' to the 'EmptyViewSet' injector"

    with pytest.raises(DependencyError) as exc_info:
        client.delete("/api/empty_set/1/")
    message = str(exc_info.value)
    assert message == "Add 'destroy' to the 'EmptyViewSet' injector"


def test_docstrings():
    """Access `api_view` and `generic_api_view` docstrings."""

    assert (
        contrib.api_view.__doc__
        == "Create DRF class-based API view from injector class."
    )
    assert (
        contrib.generic_api_view.__doc__
        == "Create DRF generic class-based API view from injector class."
    )
    assert (
        contrib.model_view_set.__doc__
        == "Create DRF model view set from injector class."
    )


def test_keep_view_informanion():
    """Generated view should point to the `Injector` subclass."""

    from django_project.api.views import UserAction, UserRetrieveView, UserViewSet

    api_view = UserAction.as_view()

    assert api_view.__name__ == "UserAction"
    assert api_view.__module__ == "django_project.api.views"
    assert api_view.__doc__ == "Intentionally left blank."

    generic_api_view = UserRetrieveView.as_view()

    assert generic_api_view.__name__ == "UserRetrieveView"
    assert generic_api_view.__module__ == "django_project.api.views"
    assert generic_api_view.__doc__ == "Intentionally left blank."

    model_view_set = UserViewSet.as_viewset()

    assert model_view_set.__name__ == "UserViewSet"
    assert model_view_set.__module__ == "django_project.api.views"
    assert model_view_set.__doc__ == "Intentionally left blank."


def test_default_throttle_scope_applied_to_default(rf, settings):
    settings.REST_FRAMEWORK = {
        "DEFAULT_THROTTLE_CLASSES": (
            "django_project.api.throttle.ThrottleDefaultScope",
        ),
    }

    @contrib.api_view
    class DefaultThrottleScope(Injector):
        get = this.command.respond
        command = project_commands.UserOperations

        throttle_scope = "throttle_scope"
        # this is the workaround for
        # https://github.com/encode/django-rest-framework/issues/6030
        throttle_classes = [project_throttle.ThrottleDefaultScope]

    # Throttle scope doesn't apply on first request.
    request = rf.get("/api/default_throttle_scope/")
    response = DefaultThrottleScope.as_view()(request)
    assert response.status_code == status.HTTP_200_OK

    # Throttle scope applies on second request.
    response = DefaultThrottleScope.as_view()(request)
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


def test_custom_throttle_scope_not_applied_to_default(rf, settings):
    settings.REST_FRAMEWORK = {
        "DEFAULT_THROTTLE_CLASSES": (
            "django_project.api.throttle.ThrottleCustomScope",
        ),
    }

    @contrib.api_view
    class DefaultThrottleScope(Injector):
        get = this.command.respond
        command = project_commands.UserOperations

        throttle_scope = "throttle_scope"
        # this is the workaround for
        # https://github.com/encode/django-rest-framework/issues/6030
        throttle_classes = [project_throttle.ThrottleCustomScope]

    request = rf.get("/api/default_throttle_scope/")

    # Throttle will always pass for default scope as it is not in settings.
    response = DefaultThrottleScope.as_view()(request)
    assert response.status_code == status.HTTP_200_OK

    response = DefaultThrottleScope.as_view()(request)
    assert response.status_code == status.HTTP_200_OK


def test_custom_throttle_scope_applied_to_custom(settings, rf):
    settings.REST_FRAMEWORK = {
        "DEFAULT_THROTTLE_CLASSES": (
            "django_project.api.throttle.ThrottleCustomScope",
        ),
    }

    @contrib.api_view
    class CustomThrottleScope(Injector):
        get = this.command.respond
        command = project_commands.UserOperations

        custom_throttle_scope = "custom_scope"
        # this is the workaround for
        # https://github.com/encode/django-rest-framework/issues/6030
        throttle_classes = [project_throttle.ThrottleCustomScope]

    # Throttle scope doesn't apply on first request.
    request = rf.get("/api/custom_throttle_scope/")
    response = CustomThrottleScope.as_view()(request)
    assert response.status_code == status.HTTP_200_OK

    # Throttle scope applies on second request.
    response = CustomThrottleScope.as_view()(request)
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

import pytest

pytest.importorskip("django")

from dependencies.contrib.rest_framework import (
    api_view,
    generic_api_view,
    model_view_set,
)
from dependencies.exceptions import DependencyError
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.auth.models import User
from polls.api.exceptions import MetadataError, NegotiationError, VersionError
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_429_TOO_MANY_REQUESTS,
)
from rest_framework.test import APIClient


client = APIClient()


def test_dispatch_request(db):
    """
    Dispatch request to the `Injector` subclass attributes.

    DRF APIView render, parser, permissions and other attributes
    should be respected.
    """

    response = client.post("/api/action/", {"last": True}, format="json")
    assert response.status_code == HTTP_200_OK
    assert response.content.decode().lstrip().startswith("<!DOCTYPE html>")

    # Parser classes mismatch.

    response = client.post("/api/action/", {"last": True})
    assert response.status_code == HTTP_415_UNSUPPORTED_MEDIA_TYPE

    # Permission classes applies.

    response = client.get("/api/login/")
    assert response.status_code == HTTP_403_FORBIDDEN

    # Authentication classes applies.

    User.objects.create(pk=1, username="johndoe", first_name="John", last_name="Doe")

    response = client.get("/api/login_all/")
    assert response.status_code == HTTP_200_OK

    # Throttle classes applies.

    response = client.get("/api/throttle_all/")
    assert response.status_code == HTTP_429_TOO_MANY_REQUESTS

    # Strict content negotiation.

    with pytest.raises(NegotiationError):
        client.get("/api/negotiate/")

    # Versioning classes applies.

    with pytest.raises(VersionError):
        client.get("/api/versioning/")

    # Metadata classes applies.

    with pytest.raises(MetadataError):
        client.options("/api/metadata/")


def test_dispatch_request_generic_view_retrieve(db):
    """
    Retrieve user details through view defined with injector subclass.
    """

    User.objects.create(pk=1, username="johndoe", first_name="John", last_name="Doe")

    response = client.get("/api/users/johndoe/", format="json")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
    }


def test_dispatch_request_generic_view_list(db):
    """
    List user details through view defined with injector subclass.
    """

    User.objects.create(pk=1, username="johndoe", first_name="John", last_name="Doe")
    User.objects.create(pk=2, username="foo", first_name="bar", last_name="baz")

    response = client.get("/api/users/?username=johndoe&limit=1", format="json")
    assert response.status_code == HTTP_200_OK
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

    User.objects.create(pk=1, username="admin", first_name="admin", last_name="admin")

    response = client.post(
        "/api/%s/" % (basename,),
        {"username": "johndoe", "first_name": "John", "last_name": "Doe"},
    )
    assert response.status_code == HTTP_201_CREATED
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
    }
    assert LogEntry.objects.filter(action_flag=ADDITION).exists()

    response = client.get("/api/%s/" % (basename,))
    assert response.status_code == HTTP_200_OK
    assert response.json() == [
        {"id": 2, "username": "johndoe", "first_name": "John", "last_name": "Doe"}
    ]

    response = client.get("/api/%s/2/" % (basename,))
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
    }

    response = client.put(
        "/api/%s/2/" % (basename,), {"username": "johndoe", "first_name": "Jim"}
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "Jim",
        "last_name": "Doe",
    }
    assert LogEntry.objects.filter(action_flag=CHANGE).exists()

    response = client.patch("/api/%s/2/" % (basename,), {"last_name": "Worm"})
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "Jim",
        "last_name": "Worm",
    }
    assert LogEntry.objects.filter(action_flag=CHANGE).count() == 2

    response = client.delete("/api/%s/2/" % (basename,))
    assert response.status_code == HTTP_204_NO_CONTENT
    assert LogEntry.objects.filter(action_flag=DELETION).exists()


def test_model_view_set_undefined_method(db):
    """
    Throw error if corresponding model view set action method is not
    defined in the injector.
    """

    User.objects.create(pk=1, username="admin", first_name="admin", last_name="admin")

    response = client.get("/api/empty_set/1/")
    assert response.status_code == HTTP_200_OK

    response = client.get("/api/empty_set/")
    assert response.status_code == HTTP_200_OK

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

    assert api_view.__doc__ == "Create DRF class-based API view from injector class."
    assert (
        generic_api_view.__doc__
        == "Create DRF generic class-based API view from injector class."
    )
    assert model_view_set.__doc__ == "Create DRF model view set from injector class."

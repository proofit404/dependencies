import pytest
from dependencies.contrib.rest_framework import (
    api_view,
    generic_api_view,
    model_view_set,
)
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


def test_dispatch_request_model_view_set(db):
    """
    List, retrieve, create, update & delete actions in the
    `ModelViewSet` defined with `Injector` subclass.
    """

    User.objects.create(pk=1, username="admin", first_name="admin", last_name="admin")

    response = client.post(
        "/api/user_set/",
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

    response = client.get("/api/user_set/")
    assert response.status_code == HTTP_200_OK
    assert response.json() == [
        {"id": 2, "username": "johndoe", "first_name": "John", "last_name": "Doe"}
    ]

    response = client.get("/api/user_set/2/")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
    }

    response = client.put(
        "/api/user_set/2/", {"username": "johndoe", "first_name": "Jim"}
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "Jim",
        "last_name": "Doe",
    }
    assert LogEntry.objects.filter(action_flag=CHANGE).exists()

    response = client.patch("/api/user_set/2/", {"last_name": "Worm"})
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "username": "johndoe",
        "first_name": "Jim",
        "last_name": "Worm",
    }
    assert LogEntry.objects.filter(action_flag=CHANGE).count() == 2

    response = client.delete("/api/user_set/2/")
    assert response.status_code == HTTP_204_NO_CONTENT
    assert LogEntry.objects.filter(action_flag=DELETION).exists()


def test_docstrings():
    """Access `api_view` and `generic_api_view` docstrings."""

    assert api_view.__doc__ == "Create DRF class-based API view from injector class."
    assert (
        generic_api_view.__doc__
        == "Create DRF generic class-based API view from injector class."
    )
    assert model_view_set.__doc__ == "Create DRF model view set from injector class."

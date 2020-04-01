# -*- coding: utf-8 -*-
import pytest


pytestmark = pytest.mark.django_db


status = pytest.importorskip("rest_framework.status")
test_client = pytest.importorskip("rest_framework.test")


client = test_client.APIClient()


def test_list_action():
    """Dispatch request to the `list` action of the generic view set."""

    response = client.get("/api/generic_view_set/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"list": "ok"}


def test_retrieve_action():
    """Dispatch request to the `retrieve` action of the generic view set."""

    response = client.get("/api/generic_view_set/1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"retrieve": "ok"}


def test_create_action():
    """Dispatch request to the `create` action of the generic view set."""

    response = client.post(
        "/api/generic_view_set/",
        {"username": "johndoe", "first_name": "John", "last_name": "Doe"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"create": "ok"}


def test_update_action():
    """Dispatch request to the `update` action of the generic view set."""

    response = client.put(
        "/api/generic_view_set/1/",
        {"username": "johndoe", "first_name": "John", "last_name": "Doe"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"update": "ok"}


def test_partial_update_action():
    """Dispatch request to the `partial_update` action of the generic view
    set."""

    response = client.patch("/api/generic_view_set/1/", {"username": "jimworm"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"partial_update": "ok"}


def test_destroy_action():
    """Dispatch request to the `destroy` action of the generic view set."""

    response = client.delete("/api/generic_view_set/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None

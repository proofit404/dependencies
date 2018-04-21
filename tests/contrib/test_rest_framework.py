from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

client = APIClient()


def test_dispatch_request():
    """
    Dispatch request to the `Injector` subclass attributes.

    DRF APIView render, parser, permissions and other attributes
    should be respected.
    """

    response = client.get("/api/questions-stat/", {"last": True}, format="json")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"details": "ok"}

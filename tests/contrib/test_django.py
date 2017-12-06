from dependencies.contrib.django import View
from django.test import RequestFactory


def test_dispatch_request():
    """Dispatch request to the `Injector` subclass attributes."""

    class Container(View):

        pass

    factory = RequestFactory()
    request = factory.get('/customer/details')

    response = Container.as_view(request)

    # assert response.status_code == 200
    assert not response

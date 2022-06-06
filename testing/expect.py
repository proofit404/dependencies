import pytest


class _Call:
    def __init__(self, container):
        self.container = container

    def __call__(self, f):
        f(self.container)


class _Context:
    def __init__(self, container):
        self.container = container

    def __call__(self, f):
        with self.container as scope:
            f(scope)


@pytest.fixture(params=[_Call, _Context])
def expect(request):
    """Access Injector subclass in different ways."""
    return request.param

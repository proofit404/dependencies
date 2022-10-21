import pytest


class _Call:
    def __init__(self, *containers):
        self.containers = containers

    def __call__(self, f):
        for container in self.containers:
            f(container)


class _Context:
    def __init__(self, *containers):
        self.containers = containers

    def __call__(self, f):
        for container in self.containers:
            with container as scope:
                f(scope)


@pytest.fixture(params=[_Call, _Context])
def expect(request):
    """Access Injector subclass in different ways."""
    return request.param

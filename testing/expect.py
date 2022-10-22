import functools

import pytest


class _Call:
    def __init__(self, *containers):
        self.containers = containers

    def __call__(self, f):
        assert f.__name__ == "case"
        for container in self.containers:
            f(it=container)


class _Context:
    def __init__(self, *containers):
        self.containers = containers

    def __call__(self, f):
        assert f.__name__ == "case"
        for container in self.containers:
            with container as scope:
                f(it=scope)


def _catch(message):
    def decorator(f):
        @functools.wraps(f)
        def inner(**kwargs):
            from dependencies.exceptions import DependencyError

            with pytest.raises(DependencyError) as exc_info:
                f(**kwargs)
            assert str(exc_info.value) == message

        return inner

    return decorator


@pytest.fixture(params=[_Call, _Context])
def expect(request):
    """Access Injector subclass in different ways."""
    return request.param


@pytest.fixture()
def catch():
    """Catch library exception."""
    return _catch

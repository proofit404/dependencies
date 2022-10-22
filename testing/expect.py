import contextlib
import functools

import pytest


class _Base:
    __used__ = False

    def __init__(self, container):
        from dependencies import Injector

        assert issubclass(container, Injector)
        self.__container__ = container

    def __call__(self, f):
        self.__class__.__used__ = True
        assert f.__name__ == "case"
        error_boundary = getattr(f, "error_boundary", contextlib.nullcontext)
        with error_boundary():
            self.__use__(f, self.__container__)


class _Injector:
    def __use__(self, f, container):
        f(it=container)

    @classmethod
    def skip_if_injector(cls):
        cls.__used__ = True
        pytest.skip()

    @classmethod
    def skip_if_scope(cls):
        pass


class _Scope:
    def __use__(self, f, container):
        with container as scope:
            f(it=scope)

    @classmethod
    def skip_if_injector(cls):
        pass

    @classmethod
    def skip_if_scope(cls):
        cls.__used__ = True
        pytest.skip()


def _catch(message):
    assert isinstance(message, str)
    message = message.strip()

    def decorator(f):
        f.error_boundary = functools.partial(_catchcontext, message)
        return f

    return decorator


@contextlib.contextmanager
def _catchcontext(message):
    from dependencies.exceptions import DependencyError

    with pytest.raises(DependencyError) as exc_info:
        yield

    assert str(exc_info.value) == message


@pytest.fixture(params=[_Injector, _Scope], ids=["injector", "scope"])
def expect(request):
    """Access Injector subclass in different ways."""

    class Expect(_Base, request.param):
        pass

    yield Expect

    assert Expect.__used__


@pytest.fixture()
def catch():
    """Catch library exception."""
    return _catch

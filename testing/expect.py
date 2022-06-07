import pytest

from dependencies.exceptions import DependencyError


class _Identity:
    def __init__(self, container):
        self.container = container

    def to(self, predicate):
        assert predicate(self.container)

    def to_raise(self, error=DependencyError):
        self.error = error
        return self

    def catch(self, function):
        with pytest.raises(self.error) as exc_info:
            function(self.container)
        return str(exc_info.value)


class _Context:
    def __init__(self, container):
        self.container = container

    def to(self, predicate):
        with self.container as scope:
            assert predicate(scope)

    def to_raise(self, error=DependencyError):
        self.error = error
        return self

    def catch(self, function):
        with pytest.raises(self.error) as exc_info, self.container as scope:
            function(scope)
        return str(exc_info.value)


@pytest.fixture(params=[_Identity, _Context])
def expect(request):
    """Access Injector subclass in different ways."""
    return request.param

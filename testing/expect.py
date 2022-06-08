import pytest

from dependencies.exceptions import DependencyError


class _Identity:
    @staticmethod
    def skip_if_context():
        pass

    def __init__(self, container):
        self.container = container

    def to(self, predicate):
        assert predicate(self.container)

    def to_raise(self, error):
        self.error = error
        return self

    def when(self, function):
        with pytest.raises(DependencyError) as exc_info:
            function(self.container)
        assert str(exc_info.value) == self.error


class _Context:
    @staticmethod
    def skip_if_context():
        pytest.skip()

    def __init__(self, container):
        self.container = container

    def to(self, predicate):
        with self.container as scope:
            assert predicate(scope)

    def to_raise(self, error):
        self.error = error
        return self

    def when(self, function):
        with pytest.raises(DependencyError) as exc_info, self.container as scope:
            function(scope)
        assert str(exc_info.value) == self.error


@pytest.fixture(params=[_Identity, _Context])
def expect(request):
    """Access Injector subclass in different ways."""
    return request.param

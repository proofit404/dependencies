import pytest

from dependencies.exceptions import DependencyError


class _Identity:
    @staticmethod
    def skip_if_context():
        pass

    def __init__(self, injector):
        self.injector = injector

    def to(self, expression):
        code = f"assert {expression}"
        scope = {"obj": self.injector}
        exec(code, scope)

    def to_raise(self, error):
        self.error = error
        return self

    def when(self, expression):
        code = f"""
with pytest.raises(DependencyError) as exc_info:
    {expression}
assert str(exc_info.value) == error
        """.strip()
        scope = {
            "pytest": pytest,
            "DependencyError": DependencyError,
            "obj": self.injector,
            "error": self.error,
        }
        exec(code, scope)


class _Context:
    @staticmethod
    def skip_if_context():
        pytest.skip()

    def __init__(self, injector):
        self.injector = injector

    def to(self, expression):
        code = f"""
with injector as obj:
    assert {expression}
        """.strip()
        scope = {"injector": self.injector}
        exec(code, scope)

    def to_raise(self, error):
        self.error = error
        return self

    def when(self, expression):
        code = f"""
with pytest.raises(DependencyError) as exc_info:
    with injector as obj:
        {expression}
assert str(exc_info.value) == error
        """.strip()
        scope = {
            "pytest": pytest,
            "DependencyError": DependencyError,
            "injector": self.injector,
            "error": self.error,
        }
        exec(code, scope)


@pytest.fixture(params=[_Identity, _Context])
def expect(request):
    """Access Injector subclass in different ways."""
    return request.param

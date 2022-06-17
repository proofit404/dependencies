import pytest


class _Identity:
    @staticmethod
    def skip_if_context():
        pass

    def __init__(self, coder):
        self.coder = coder

    def __call__(self, injector):
        self.injector = injector
        return self

    def to(self, *expressions):
        assert expressions
        self.coder.write(
            f"def test_case():\n    obj = {self.injector}\n"
            + "".join(f"    assert {expression}\n" for expression in expressions)
        )
        self.coder.run()

    def to_raise(self, error):
        self.error = error.strip()
        return self

    def when(self, expression):
        self.coder.write(
            f"""
def test_case():
    obj = {self.injector}
    with pytest.raises(DependencyError) as exc_info:
        {expression}
    assert str(exc_info.value) == f{self.error!r}
            """.lstrip()
        )
        self.coder.run()


class _Context:
    @staticmethod
    def skip_if_context():
        pytest.skip()

    def __init__(self, coder):
        self.coder = coder

    def __call__(self, injector):
        self.injector = injector
        return self

    def to(self, *expressions):
        assert expressions
        self.coder.write(
            f"def test_case():\n    with {self.injector} as obj:\n"
            + "".join(f"        assert {expression}\n" for expression in expressions)
        )
        self.coder.run()

    def to_raise(self, error):
        self.error = error.strip()
        return self

    def when(self, expression):
        self.coder.write(
            f"""
def test_case():
    with pytest.raises(DependencyError) as exc_info:
        with {self.injector} as obj:
            {expression}
    assert str(exc_info.value) == f{self.error!r}
            """
        )
        self.coder.run()


@pytest.fixture(params=[_Identity, _Context], ids=["pass", "context"])
def expect(request, coder):
    """Access Injector subclass in different ways."""
    return request.param(coder)

import pytest


class CodeCollector:
    """Dedicated decorator to use functions as Py.Test function parameters."""

    def __init__(self, name="code"):

        self.name = name
        self.collected = []

    def __call__(self, f):
        """Mark decorated function as a test parameter."""
        self.collected.append(f)
        return f

    def xfail(self, f):
        """Mark function as a test parameter with expected failure."""
        return self(pytest.param(f, marks=pytest.mark.xfail))

    def __iter__(self):
        return iter(self.collected)

    def parametrize(self, test_func):
        """Parametrize decorated test function with collected functions."""
        return pytest.mark.parametrize(self.name, self)(test_func)

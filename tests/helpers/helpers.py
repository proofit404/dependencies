import random
import string

import pytest


class CodeCollector:
    """Dedicated decorator to use functions as Py.Test function parameters."""

    def __init__(self, name="code"):
        self.name = name
        self.collected = []

    def parametrize(self, test_func):
        """Parametrize decorated test function with collected functions."""
        return pytest.mark.parametrize(self.name, iter(self.collected))(test_func)

    def __call__(self, f):
        """Mark decorated function as a test parameter."""
        self._validate(f)
        return self._add(f)

    def xfail(self, f):
        """Mark function as a test parameter with expected failure."""
        self._validate(f)
        return self._add(pytest.param(f, marks=pytest.mark.xfail))

    def _validate(self, f):
        function_name = f.__name__
        _validate_uniqueness(function_name, self.collected)
        _validate_length(function_name)
        _validate_prefix(function_name)
        _validate_tail(function_name)

    def _add(self, arg):
        self.collected.append(arg)
        return arg


def _validate_uniqueness(name, collection):
    if name in collection:  # pragma: no cover
        raise Exception(f"{name} was already collected")


def _validate_length(name):
    if len(name) != 13:  # pragma: no cover
        raise Exception(f"{name} should be 13 characters long")


def _validate_prefix(name):
    if not name.startswith("_"):  # pragma: no cover
        raise Exception(f"{name} should be a private function")


def _validate_tail(name):
    for char in name[1:]:
        if char not in string.ascii_letters + string.digits:  # pragma: no cover
            suggested = _suggest()
            message = wrong_name_template.format(
                function_name=name, suggested=suggested
            )
            raise Exception(message)


def _suggest():  # pragma: no cover
    return (
        "_"
        + random.choice(string.ascii_lowercase)
        + "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(11)
        )
    )


# Messages.


wrong_name_template = """
{function_name} should a have random name.

How about {suggested!r}
""".strip()

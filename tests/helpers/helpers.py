import functools
import inspect
import random
import re
import string

import pytest


class CodeCollector:
    """Dedicated decorator to use functions as Py.Test function parameters."""

    seen = set()

    def __init__(self, *names):
        self.names = names or ("code",)
        self.collected = []

    def parametrize(self, test_func):
        """Parametrize decorated test function with collected functions."""
        iterable = _Iterable(test_func.__name__, self.collected)
        return pytest.mark.parametrize(self.names, iterable)(test_func)

    def __call__(self, *args):
        """Mark decorated function as a test parameter."""
        if not self._is_complete(args):
            return functools.partial(self.__call__, *args)
        f = args[-1]
        self._validate(f)
        self._remember(f)
        self._add(args)
        return f

    def _is_complete(self, args):
        return len(self.names) == len(args)

    def _validate(self, f):
        _validate_function(f)
        _validate_uniqueness(f, self.seen)
        _validate_length(f)
        _validate_prefix(f)
        _validate_tail(f)
        _validate_assert_statement(f)

    def _remember(self, f):
        self.seen.add(f.__name__)

    def _add(self, arg):
        self.collected.append(arg)


class _Iterable:
    def __init__(self, test_name, data):
        self.test_name = test_name
        self.data = data

    def __iter__(self):
        return _Iterator(self.test_name, self.data)


class _Iterator:
    def __init__(self, test_name, data):
        self.test_name = test_name
        self.data = data
        self.state = iter(data)

    def __next__(self):
        _validate_collected(self.test_name, self.data)
        return next(self.state)


def _validate_collected(test_name, collected):
    if not collected:  # pragma: no cover
        raise Exception("No functions was collected")
    elif len(collected) == 1:  # pragma: no cover
        message = single_item_collected.format(test_func=test_name)
        raise Exception(message)


def _validate_function(function):
    if not callable(function):  # pragma: no cover
        raise Exception("Last argument should be a function")


def _validate_uniqueness(function, seen):
    if function.__name__ in seen:  # pragma: no cover
        suggested = _suggest()
        message = repeated_template.format(
            function_name=function.__name__, suggested=suggested
        )
        raise Exception(message)


def _validate_length(function):
    if len(function.__name__) != 13:  # pragma: no cover
        suggested = _suggest()
        message = wrong_length_template.format(
            function_name=function.__name__, suggested=suggested
        )
        raise Exception(message)


def _validate_prefix(function):
    if not function.__name__.startswith("_"):  # pragma: no cover
        suggested = _suggest()
        message = wrong_prefix_template.format(
            function_name=function.__name__, suggested=suggested
        )
        raise Exception(message)


def _validate_tail(function):
    for char in function.__name__[1:]:
        if char not in string.ascii_letters + string.digits:  # pragma: no cover
            suggested = _suggest()
            message = wrong_name_template.format(
                function_name=function.__name__, suggested=suggested
            )
            raise Exception(message)


def _suggest():  # pragma: no cover
    head = random.choice(string.ascii_lowercase)
    tail = (random.choice(string.ascii_letters + string.digits) for _ in range(11))
    return "_" + head + "".join(tail)


def _validate_assert_statement(function):
    source = inspect.getsource(function)
    if re.search(r"\bassert\b", source):  # pragma: no cover
        message = assert_found_template.format(function_name=function.__name__)
        raise Exception(message)


# Messages.


single_item_collected = """
Only one function was collected as test parameter.

Collect more functions or inline parameter inside test.

Inspect {test_func} definition.
""".strip()


repeated_template = """
{function_name} was already collected.

How about {suggested}
""".strip()


wrong_length_template = """
{function_name} should be 13 characters long.

How about {suggested}
""".strip()


wrong_prefix_template = """
{function_name} should be a private function.

How about {suggested}
""".strip()


wrong_name_template = """
{function_name} should a have random name.

How about {suggested}
""".strip()


assert_found_template = """
{function_name} contains assert statement.

All assert statements should be placed in the parametrized test.
""".strip()

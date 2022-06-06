from random import choice
from random import randint
from string import ascii_letters

import pytest

from dependencies import Injector


def _subclass(*args, **kwargs):
    scope = {}
    variables = {}

    for attribute, dependency in kwargs.items():
        lookup = _random_string()
        variables[attribute] = lookup
        scope[lookup] = dependency

    name = _random_string().title()

    base = _random_string().title()
    scope[base] = (args or (Injector,))[0]

    body = "".join(f"    {a} = {l}\n" for a, l in variables.items())

    code = f"class {name}({base}):\n{body}"

    exec(code, scope)

    return scope[name]


def _call(*args, **kwargs):
    return (args or (Injector,))[0](**kwargs)


def _random_string():
    return "".join(choice(ascii_letters) for i in range(randint(8, 24)))


@pytest.fixture(params=[_subclass, _call])
def has(request):
    """Inherit from Injector in different ways."""
    return request.param

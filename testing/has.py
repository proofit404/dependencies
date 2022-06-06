from random import choice
from random import randint
from string import ascii_letters

import pytest

from dependencies import Injector


def _subclass(*args, **kwargs):
    scope = {}
    bases = []
    variables = []

    for base in args or (Injector,):
        lookup = _random_string()
        bases.append(lookup)
        scope[lookup] = base

    for attribute, dependency in kwargs.items():
        lookup = _random_string()
        variables.append((attribute, lookup))
        scope[lookup] = dependency

    name = _random_string().title()

    bases = ", ".join(bases)

    if variables:
        body = "".join(f"    {a} = {l}\n" for a, l in variables)
    else:
        body = "    ...\n"

    code = f"class {name}({bases}):\n{body}"

    exec(code, scope)

    return scope[name]


def _call(*args, **kwargs):
    scope = {}
    bases = []
    variables = []

    for base in args or (Injector,):
        lookup = _random_string()
        bases.append(lookup)
        scope[lookup] = base

    for attribute, dependency in kwargs.items():
        lookup = _random_string()
        variables.append((attribute, lookup))
        scope[lookup] = dependency

    name = _random_string().title()

    bases = " & ".join(bases)

    if variables:
        body = "(" + ", ".join(f"{a}={l}" for a, l in variables) + ")"
        if len(args) > 1:
            bases = "(" + bases + ")"
    else:
        body = ""

    code = f"{name} = {bases}{body}"

    exec(code, scope)

    return scope[name]


def _random_string():
    return "".join(choice(ascii_letters) for i in range(randint(8, 24)))


@pytest.fixture(params=[_subclass, _call])
def has(request):
    """Inherit from Injector in different ways."""
    return request.param

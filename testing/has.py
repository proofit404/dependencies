from random import choice
from random import randint
from string import ascii_letters

import pytest

from let import Class
from let import Function


class _Subclass:
    def __init__(self, coder):
        self.coder = coder

    def __call__(self, *args, **kwargs):
        name = _random_string().title()
        bases = ", ".join(args or ("Injector",))
        if kwargs:
            body = "".join(f"    {k} = {_ref(v)}\n" for k, v in kwargs.items())
        else:
            body = "    pass\n"
        self.coder.write(
            f"""
class {name}({bases}):
{body}
            """
        )
        return name


class _Call:
    def __init__(self, coder):
        self.coder = coder

    def __call__(self, *args, **kwargs):
        name = _random_string().title()
        bases = " & ".join(args or ("Injector",))
        if kwargs:
            body = "(" + ", ".join(f"{k}={_ref(v)}" for k, v in kwargs.items()) + ")"
            if len(args) > 1:
                bases = "(" + bases + ")"
        elif len(args) > 1:
            body = ""
        else:
            body = "()"
        self.coder.write(
            f"""
{name} = {bases}{body}
            """
        )
        return name


def _random_string():
    return "".join(choice(ascii_letters) for i in range(randint(8, 24)))


def _ref(v):
    if isinstance(v, (Class, Function)):
        return v.name
    elif isinstance(v, str):
        return v
    else:
        raise RuntimeError


@pytest.fixture(params=[_Subclass, _Call])
def has(request, coder):
    """Inherit from Injector in different ways."""
    return request.param(coder)


@pytest.fixture()
def name():
    """Generate expression to access Injector name."""
    return lambda of: "{" + of + ".__name__}"

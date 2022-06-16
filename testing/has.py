from random import choice
from random import randint
from string import ascii_letters
from textwrap import indent

import pytest

from let import _Class
from let import _Function


class _Subclass:
    def __init__(self, coder):
        self.coder = coder

    def __call__(self, *args, **kwargs):
        name = _random_string().title()
        bases = ", ".join(args or ("Injector",))
        if kwargs:
            body = "".join(self.ref(k, v) for k, v in kwargs.items())
        else:
            body = "    pass\n"
        self.coder.write(
            f"""
class {name}({bases}):
{body}
            """
        )
        return name

    def ref(self, k, v):
        if isinstance(v, (_Class, _Function)):
            if not v.defined:
                # FIXME: Should we replace `v.name` with `k` here?
                # Maybe introduce `rename` method which would return
                # brand new instance.
                return indent(v, "    ")
            v = v.name
        if isinstance(v, str):
            return f"    {k} = {v}\n"
        else:
            raise RuntimeError


class _Call:
    def __init__(self, coder):
        self.coder = coder

    def __call__(self, *args, **kwargs):
        name = _random_string().title()
        bases = " & ".join(args or ("Injector",))
        if kwargs:
            body = "(" + ", ".join(self.ref(k, v) for k, v in kwargs.items()) + ")"
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

    def ref(self, k, v):
        if isinstance(v, (_Class, _Function)):
            if not v.defined:
                self.coder.write(v)
                v.defined = True
            v = v.name
        if isinstance(v, str):
            return f"{k}={v}"
        else:
            raise RuntimeError


def _random_string():
    return "".join(choice(ascii_letters) for i in range(randint(8, 24)))


@pytest.fixture(params=[_Subclass, _Call], ids=["class", "call"])
def has(request, coder):
    """Inherit from Injector in different ways."""
    return request.param(coder)


@pytest.fixture()
def name():
    """Generate expression to access Injector name."""
    return lambda of: "{" + of + ".__name__}"

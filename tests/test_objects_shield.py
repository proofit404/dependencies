"""Tests related to Shield object."""
from dependencies import Injector
from dependencies import shield
from dependencies import this


def test_pass_args(e):
    """Pass positional arguments."""

    class Container(Injector):
        result = shield(e.StarArgs, 1, 2)

    assert Container.result.args == (1, 2)


def test_pass_args_this(e):
    """Pass resolved this object as positional arguments."""

    class Container(Injector):
        result = shield(e.StarArgs, this.a, this.b)
        a = 1
        b = 2

    assert Container.result.args == (1, 2)

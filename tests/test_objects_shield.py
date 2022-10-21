"""Tests related to Shield object."""
from dependencies import Injector
from dependencies import Package
from dependencies import shield
from dependencies import this


def test_pass_args(e, expect):
    """Pass positional arguments."""

    class Container(Injector):
        result = shield(e.StarArgs, 1, 2)

    @expect(Container)
    def to_be(it):
        assert it.result.args == (1, 2)


def test_pass_args_this(e, expect):
    """Pass resolved this object as positional arguments."""

    class Container(Injector):
        result = shield(e.StarArgs, this.a, this.b)
        a = 1
        b = 2

    @expect(Container)
    def to_be(it):
        assert it.result.args == (1, 2)


def test_pass_args_package(e, expect):
    """Pass resolved package object as positional arguments."""
    examples = Package("examples")

    class Container(Injector):
        result = shield(e.StarArgs, examples.a, examples.b)

    @expect(Container)
    def to_be(it):
        assert it.result.args == (1, 2)

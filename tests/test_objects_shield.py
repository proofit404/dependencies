"""Tests related to Shield object."""
from dependencies import Injector
from dependencies import shield


def test_pass_args(e, expect):
    """Pass positional arguments."""

    class Container(Injector):
        result = shield(e.StarArgs, 1, 2)

    @expect(Container)
    def case(it):
        assert it.result.args == (1, 2)

"""Tests related to Shield object."""
from dependencies import Injector
from dependencies import shield


def test_pass_args():
    """Pass positional arguments."""

    class Result:
        def __init__(self, *args):
            self.args = args

    class Container(Injector):
        result = shield(Result, 1, 2)

    assert Container.result.args == (1, 2)

"""Tests related to the `this` object checks."""
import pytest

from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


direct_proxy = CodeCollector()


@direct_proxy.parametrize
def test_deny_this_without_attribute_access(code):
    """`this` object can't be used as a dependency directly."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    message = str(exc_info.value)
    assert message == "You can not use 'this' directly in the 'Injector'"


@direct_proxy
def _b648b6f6a712():
    class Container(Injector):
        foo = this


@direct_proxy
def _c147d398f4be():
    class Container(Injector):
        foo = this << 1


@direct_proxy
def _a37783b6d1ad():
    Injector(foo=this)


@direct_proxy
def _bd05271fb831():
    Injector(foo=(this << 1))

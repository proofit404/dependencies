"""Tests related to scalar types."""
import pytest

from collector import CodeCollector
from dependencies import Injector
from dependencies.exceptions import DependencyError


deny_direct_resolve = CodeCollector()


@deny_direct_resolve.parametrize
def test_direct_data_resolve(touch, code):
    """Attempt to resolve scalar types directly should raise exception.

    Scalar types are allowed to be used as dependencies for classes.

    """
    with pytest.raises(DependencyError) as exc_info:
        touch(code(), "a")
    expected = "Scalar dependencies could only be used to instantiate classes"
    assert str(exc_info.value) == expected


@deny_direct_resolve
def _jxu5tzdy99V7():
    class Container(Injector):
        a = 1

    return Container


@deny_direct_resolve
def _z8iAExxZyJjd():
    return Injector(a=1)

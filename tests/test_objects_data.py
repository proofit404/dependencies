"""Tests related to scalar types."""
import pytest

from dependencies import Injector
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


deny_data = CodeCollector()


@deny_data.parametrize
def test_data(code):
    """Attempt to resolve scalar types directly should raise exception.

    Scalar types are allowed to be used as dependencies for classes.

    """
    with pytest.raises(DependencyError) as exc_info:
        code()
    expected = "Scalar dependencies could only be used to instantiate classes"
    assert str(exc_info.value) == expected


@deny_data
def _jxu5tzdy99V7():
    class Container(Injector):
        a = 1

    Container.a


@deny_data
def _z8iAExxZyJjd():
    Injector(a=1).a

"""Tests related to direct resolve rules."""
import pytest

from dependencies import Injector
from dependencies import Package
from dependencies import this
from dependencies import value
from dependencies.exceptions import DependencyError


def test_direct_data_resolve(expect):
    """Attempt to resolve scalar types directly should raise exception.

    Scalar types are allowed to be used as dependencies for classes.

    """

    class Container(Injector):
        a = 1

    @expect(Container)
    def to_be(it):
        with pytest.raises(DependencyError) as exc_info:
            it.a
        expected = "Scalar dependencies could only be used to instantiate classes"
        assert str(exc_info.value) == expected


def test_direct_this_resolve(expect):
    """Attempt to resolve this directly should raise exception.

    This objects are allowed to be used as dependencies for classes.

    """

    class Container(Injector):
        a = this.b
        b = 1

    @expect(Container)
    def to_be(it):
        with pytest.raises(DependencyError) as exc_info:
            it.a
        expected = "'this' dependencies could only be used to instantiate classes"
        assert str(exc_info.value) == expected


def test_direct_nested_injector_resolve(expect):
    """Attempt to resolve nested injector directly should raise exception.

    Nested injectors are allowed to be used as this object targets.

    """

    class Container(Injector):
        class Nested(Injector):
            foo = 1

    @expect(Container)
    def to_be(it):
        with pytest.raises(DependencyError) as exc_info:
            it.Nested
        expected = "'Injector' dependencies could only be used to instantiate classes"
        assert str(exc_info.value) == expected


def test_direct_value_resolve(expect):
    """Attempt to resolve value directly should raise exception.

    Values are allowed to be used as dependencies for classes.

    """

    class Container(Injector):
        @value
        def a():
            return 1

    @expect(Container)
    def to_be(it):
        with pytest.raises(DependencyError) as exc_info:
            it.a
        expected = "'value' dependencies could only be used to instantiate classes"
        assert str(exc_info.value) == expected


def test_direct_package_data_resolve(expect):
    """Attempt to resolve scalar types directly should raise exception."""
    examples = Package("examples")

    class Container(Injector):
        a = examples.submodule.variable

    @expect(Container)
    def to_be(it):
        with pytest.raises(DependencyError) as exc_info:
            it.a
        expected = "Scalar dependencies could only be used to instantiate classes"
        assert str(exc_info.value) == expected


def test_direct_package_class_resolve(expect):
    """Attempt to resolve class directly should works for packages."""
    from examples.submodule import Foo

    examples = Package("examples")

    class Container(Injector):
        foo = examples.submodule.Foo

    @expect(Container)
    def to_be(it):
        assert isinstance(it.foo, Foo)

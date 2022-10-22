"""Tests related to direct resolve rules."""
from dependencies import Injector
from dependencies import value


def test_direct_data_resolve(expect, catch):
    """Attempt to resolve scalar types directly should raise exception.

    Scalar types are allowed to be used as dependencies for classes.

    """

    class Container(Injector):
        a = 1

    @expect(Container)
    @catch("Scalar dependencies could only be used to instantiate classes")
    def case(it):
        it.a


def test_direct_nested_injector_resolve(expect, catch):
    """Attempt to resolve nested injector directly should raise exception.

    Nested injectors are allowed to be used as this object targets.

    """

    class Container(Injector):
        class Nested(Injector):
            foo = 1

    @expect(Container)
    @catch("'Injector' dependencies could only be used to instantiate classes")
    def case(it):
        it.Nested


def test_direct_value_resolve(expect, catch):
    """Attempt to resolve value directly should raise exception.

    Values are allowed to be used as dependencies for classes.

    """

    class Container(Injector):
        @value
        def a():
            return 1

    @expect(Container)
    @catch("'value' dependencies could only be used to instantiate classes")
    def case(it):
        it.a

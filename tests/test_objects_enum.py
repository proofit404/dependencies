"""Tests related to enum objects."""
from enum import auto
from enum import Enum
from enum import unique

from dependencies import Injector


@unique
class Choices(Enum):
    """Enumeration class."""

    one = auto()
    two = auto()
    three = auto()


def test_deny_enums(expect, catch):
    """Deny inject enum classes.

    We should suggest to inject a specific enum member instead.

    """

    class Container(Injector):
        choices = Choices

    @expect(Container)
    @catch(
        """
Attribute 'choices' contains Enum.

Do not inject enumeration classes.

It will be unable to instantiate this class.

Inject its members instead.
        """
    )
    def case(it):
        it.foo


def test_allow_enum_members(e, expect):
    """Allow to inject enum members."""

    class Container(Injector):
        foo = e.Take["choice"]
        choice = Choices.one

    @expect(Container)
    def case(it):
        assert it.foo is Choices.one


def test_allow_class_named_enum(e, expect):
    """Allow to inject enum classes using class-named attributes."""

    class Container(Injector):
        foo = e.Take["choices_class"]
        choices_class = Choices

    @expect(Container)
    def case(it):
        assert it.foo is Choices

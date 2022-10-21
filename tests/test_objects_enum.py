"""Tests related to enum objects."""
from enum import auto
from enum import Enum
from enum import unique

import pytest

from dependencies import Injector
from dependencies.exceptions import DependencyError


@unique
class Choices(Enum):
    """Enumeration class."""

    one = auto()
    two = auto()
    three = auto()


def test_deny_enums():
    """Deny inject enum classes.

    We should suggest to inject a specific enum member instead.

    """

    class Foo:
        pass

    class Container(Injector):
        foo = Foo
        choices = Choices

    with pytest.raises(DependencyError) as exc_info:
        Container.foo

    expected = """
Attribute 'choices' contains Enum.

Do not inject enumeration classes.

It will be unable to instantiate this class.

Inject its members instead.
    """.strip()

    assert str(exc_info.value) == expected


def test_allow_enum_members():
    """Allow to inject enum members."""

    class Foo:
        def __init__(self, choice):
            self.choice = choice

    class Container(Injector):
        foo = Foo
        choice = Choices.one

    assert Container.foo.choice is Choices.one


def test_allow_class_named_enum():
    """Allow to inject enum classes using class-named attributes."""

    class Foo:
        def __init__(self, choices_class):
            self.choices_class = choices_class

    class Container(Injector):
        foo = Foo
        choices_class = Choices

    assert Container.foo.choices_class is Choices

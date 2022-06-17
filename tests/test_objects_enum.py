# FIXME: This should be tested with `Package` as well.
"""Tests related to enum objects."""
from enum import auto
from enum import Enum
from enum import unique

import pytest

from collector import CodeCollector
from dependencies import Injector
from dependencies.exceptions import DependencyError


@unique
class Choices(Enum):
    """Enumeration class."""

    one = auto()
    two = auto()
    three = auto()


deny_enums = CodeCollector()


@deny_enums.parametrize
def test_deny_enums(code):
    """Deny inject enum classes.

    We should suggest to inject a specific enum member instead.

    """

    class Foo:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    expected = """
Attribute 'choices' contains Enum.

Do not inject enumeration classes.

It will be unable to instantiate this class.

Inject its members instead.
    """.strip()

    assert str(exc_info.value) == expected


@deny_enums
def _xO4I429TCjk6(Foo):
    class Container(Injector):
        foo = Foo
        choices = Choices

    Container.foo


@deny_enums
def _bfShH49KZHzO(Foo):
    Injector(foo=Foo, choices=Choices).foo


allow_enum_members = CodeCollector()


@allow_enum_members.parametrize
def test_allow_enum_members(code):
    """Allow to inject enum members."""

    class Foo:
        def __init__(self, choice):
            self.choice = choice

    foo = code(Foo)
    assert foo.choice is Choices.one


@allow_enum_members
def _jn7EXz98BASo(Foo):
    class Container(Injector):
        foo = Foo
        choice = Choices.one

    return Container.foo


@allow_enum_members
def _akyelo6E7WLU(Foo):
    return Injector(
        foo=Foo,
        choice=Choices.one,
    ).foo


allow_class_named_enum = CodeCollector()


@allow_class_named_enum.parametrize
def test_allow_class_named_enum(code):
    """Allow to inject enum classes using class-named attributes."""

    class Foo:
        def __init__(self, choices_class):
            self.choices_class = choices_class

    foo = code(Foo)
    assert foo.choices_class is Choices


@allow_class_named_enum
def _zbx0Ur6z6qLa(Foo):
    class Container(Injector):
        foo = Foo
        choices_class = Choices

    return Container.foo


@allow_class_named_enum
def _yhbeVQuEZeTk(Foo):
    return Injector(
        foo=Foo,
        choices_class=Choices,
    ).foo

"""Tests related to injection scope extension."""
import pytest

from dependencies import Injector
from dependencies.exceptions import DependencyError


def test_deny_injector_attribute_assignment(expect, catch):
    """Deny attribute assignment on `Injector` and its subclasses."""

    class Container(Injector):
        foo = 1

    @expect(Container)
    @catch("'Injector' modification is not allowed")
    def case(it):
        it.foo = 1

    @expect(Injector)
    @catch("'Injector' modification is not allowed")
    def case(it):
        it.foo = 1


def test_deny_injector_attribute_deletion(expect, catch):
    """Deny attribute deletion on `Injector` and its subclasses."""

    class Container(Injector):
        foo = 1

    @expect(Container)
    @catch("'Injector' modification is not allowed")
    def case(it):
        del it.foo

    @expect(Injector)
    @catch("'Injector' modification is not allowed")
    def case(it):
        del it.foo


def test_extension_is_subclass():
    """`Injector` with extended scope is new subclass of orgininal `Injector`."""

    class Container1(Injector):
        x = 1

    class Container2(Container1):
        y = 2

    assert issubclass(Container2, Container1)
    assert issubclass(Container1(y=2), Container1)


def test_extension_base(e, expect):
    """`Injector` could be called directly."""

    class Container(Injector):
        null = e.Null

    @expect(Container)
    def case(it):
        assert isinstance(it.null, e.Null)

    @expect(Injector(null=e.Null))
    def case(it):
        assert isinstance(it.null, e.Null)


def test_extension_add(e, expect):
    """Extended scope could add new dependencies."""

    class Container1(Injector):
        foo = e.Take["bar"]

    class Container2(Container1):
        bar = 1

    @expect(Container2)
    def case(it):
        assert it.foo == 1

    @expect(Container1(bar=2))
    def case(it):
        assert it.foo == 2


def test_extension_overwrite(e, expect):
    """Extended scope could redefine existed dependencies."""

    class Container1(Injector):
        bar = e.Take["baz"]
        baz = 1

    class Container2(Container1):
        baz = 2

    @expect(Container2)
    def case(it):
        assert it.bar == 2

    @expect(Container1(baz=3))
    def case(it):
        assert it.bar == 3


def test_deny_empty_extension():
    """`Injector` subclasses can't extend scope with empty subset."""
    with pytest.raises(DependencyError) as exc_info:

        class Foo(Injector):
            pass

    assert str(exc_info.value) == "Extension scope can not be empty"

    with pytest.raises(DependencyError) as exc_info:
        Injector()

    assert str(exc_info.value) == "Extension scope can not be empty"

    class Container(Injector):
        x = 1

    with pytest.raises(DependencyError) as exc_info:

        class Bar(Container):
            pass

    assert str(exc_info.value) == "Extension scope can not be empty"

    with pytest.raises(DependencyError) as exc_info:
        Container()

    assert str(exc_info.value) == "Extension scope can not be empty"


def test_concatenation_is_subclass(e):
    """Concatenation result is Injector subclass itself."""

    class Container1(Injector):
        a = e.Null

    class Container2(Injector):
        b = e.Has["a"]

    class Container3(Injector):
        c = e.Has["b"]

    class Container4(Container1, Container2, Container3):
        pass

    assert issubclass(Container4, Container1)
    assert issubclass(Container4, Container2)
    assert issubclass(Container4, Container3)

    assert issubclass((Container1 & Container2 & Container3), Container1)
    assert issubclass((Container1 & Container2 & Container3), Container2)
    assert issubclass((Container1 & Container2 & Container3), Container3)


def test_concatenation_add(e, expect):
    """We could concatenate multiple injectors into a new one."""

    class Container1(Injector):
        a = e.Null

    class Container2(Injector):
        b = e.Has["a"]

    class Container3(Injector):
        c = e.Has["b"]

    class Container4(Container1, Container2, Container3):
        pass

    @expect(Container4)
    def case(it):
        assert isinstance(it.c.b.a, e.Null)

    @expect(Container1 & Container2 & Container3)
    def case(it):
        assert isinstance(it.c.b.a, e.Null)


def test_concatenation_override(e, expect):
    """Order of `Injector` subclasses should affect injection result.

    `Injector` which comes first in the subclass bases or inplace creation must have
    higher precedence.

    """

    class Container1(Injector):
        foo = e.Take["x"]
        x = 1

    class Container2(Injector):
        x = 2

    class Container3(Injector):
        x = 3

    class Container4(Container1, Container2, Container3):
        pass

    class Container5(Container2, Container3, Container1):
        pass

    class Container6(Container3, Container2, Container1):
        pass

    @expect(Container4)
    def case(it):
        assert it.foo == 1

    @expect(Container5)
    def case(it):
        assert it.foo == 2

    @expect(Container6)
    def case(it):
        assert it.foo == 3

    @expect(Container1 & Container2 & Container3)
    def case(it):
        assert it.foo == 1

    @expect(Container2 & Container3 & Container1)
    def case(it):
        assert it.foo == 2

    @expect(Container3 & Container2 & Container1)
    def case(it):
        assert it.foo == 3


def test_deny_different_types_concatenation(e):
    """Only `Injector` subclasses are allowed to be concatenated."""
    with pytest.raises(DependencyError) as exc_info:

        class Bar(Injector, e.Null):
            pass

    assert str(exc_info.value) == "Multiple inheritance requires Injector subclass"

    with pytest.raises(DependencyError) as exc_info:
        Injector & e.Null

    assert str(exc_info.value) == "Multiple inheritance requires Injector subclass"

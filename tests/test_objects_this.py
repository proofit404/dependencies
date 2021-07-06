"""Tests related to the `this` object."""
import pytest

from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


def test_attribute_getter():
    """We can describe attribute access in the `Injector` in declarative manner."""

    class Foo:
        def __init__(self, one, two):
            self.one = one
            self.two = two

        def do(self):
            return self.one + self.two

    class Container(Injector):
        class SubContainer(Injector):
            foo = Foo
            one = 1
            two = 2

        foo = this.SubContainer.foo

    foo = Container.foo
    assert isinstance(foo, Foo)
    assert foo.do() == 3


def test_attribute_getter_few_attributes():
    """We resolve attribute access until we find all specified attributes."""

    class Foo:
        def __init__(self, one):
            self.one = one

    class Container(Injector):
        class SubContainer(Injector):
            foo = Foo
            one = 1

        foo = this.SubContainer.foo.one

    assert Container.foo == 1


item_access = CodeCollector()


@item_access.parametrize
@pytest.mark.xfail()
def test_item_getter(code):
    """We can describe item access in the `Injector` in the declarative manner."""
    result = code()
    assert result == 1  # pragma: no cover


@item_access
def _ce642f492941():
    class Container(Injector):
        foo = {"one": 1}
        one = this.foo["one"]

    result = Container.one

    return result  # pragma: no cover


@item_access
def _ffa208dc1130():
    class Container(Injector):
        foo = {"one": {"two": 1}}
        two = this.foo["one"]["two"]

    result = Container.two

    return result  # pragma: no cover


@item_access
def _e5c358190fef():
    class Container(Injector):
        foo = {"bar": {"baz": 1}}

        class SubContainer(Injector):
            spam = (this << 1).foo["bar"]["baz"]

    result = Container.SubContainer.spam

    return result  # pragma: no cover


@item_access
def _ab4cdbf60b2f():
    class Container(Injector):
        foo = {"bar": {"baz": 1}}

        class SubContainer(Injector):
            class SubSubContainer(Injector):
                spam = (this << 2).foo["bar"]["baz"]

    result = Container.SubContainer.SubSubContainer.spam

    return result  # pragma: no cover


@item_access
def _be332433b74d():
    class Container(Injector):
        foo = [1, 2, 3]
        bar = this.foo[0]

    result = Container.bar

    return result  # pragma: no cover


@item_access
def _fe150d5ebe93():
    class Container(Injector):
        foo = {2: 1}
        bar = this.foo[2]

    result = Container.bar

    return result  # pragma: no cover


@item_access
def _dc4fedcd09d8():
    class Container(Injector):
        foo = {("x", 1): 1}
        bar = this.foo[("x", 1)]

    result = Container.bar

    return result  # pragma: no cover


@pytest.mark.xfail()
def test_item_getter_non_printable_key():
    """Don't use string representation as key hash function.

    We can describe item access for keys which can't be presented as normal strings.

    """

    class Boom:
        def __init__(self, salt):
            self.salt = salt

        def __hash__(self):
            return hash(self.salt)

        def __str__(self):
            return "<boom>"  # pragma: no cover

    boom = Boom("hello")

    class Container(Injector):
        foo = {boom: 1}
        bar = this.foo[boom]

    assert Container.bar == 1


def test_attribute_access_after_item_getter():
    """Check we can use attribute access notation after item getter notation."""

    class Foo:
        x = 1

    class Bar:
        y = {"foo": Foo}

    class Container(Injector):
        bar = Bar
        baz = this.bar.y["foo"].x

    assert Container.baz == 1


def test_this_deny_non_integers():
    """We can't shift `this` with non number argument."""
    with pytest.raises(ValueError, match=".*") as exc_info:
        this << "boom"

    assert str(exc_info.value) == "Positive integer argument is required"


negative_integers = CodeCollector()


@negative_integers.parametrize
def test_this_deny_negative_integers(code):
    """We can't shift `this` with negative integer."""
    with pytest.raises(ValueError, match=".*") as exc_info:
        code()

    assert str(exc_info.value) == "Positive integer argument is required"


@negative_integers
def _xsJWb2lx6EMs():
    this << -1


@negative_integers
def _nvm3ybp98vGm():
    this << 0


too_many = CodeCollector()


@too_many.parametrize
def test_require_more_parents_that_injector_actually_has(code):
    """Verify `this` expression against depth of nesting.

    If we shift more that container levels available, we should provide meaningful
    message to user.

    """
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == (
        "You tried to shift this more times than Injector has levels"
    )


@too_many
def _s6lduD7BJpxW():
    class Container(Injector):

        foo = (this << 1).bar

    Container.foo


@too_many
def _bUICVObtDZ4I():
    class Container(Injector):
        class SubContainer(Injector):

            foo = (this << 2).bar

    Container.SubContainer.foo


@too_many
def _ww6xNI4YrNr6():
    Injector(foo=(this << 1).bar).foo


@too_many
def _rN3suiVzhqMM():
    Injector(SubContainer=Injector(foo=(this << 2).bar)).SubContainer.foo


attribute_error = CodeCollector()


@attribute_error.parametrize
def test_attribute_error_on_parent_access(code):
    """Verify `this` object expression against existed dependencies.

    We should raise `AttributeError` if we have correct number of parents but specify
    wrong attribute name.

    """
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) in {
        "'Container' can not resolve attribute 'bar'",
        "'Injector' can not resolve attribute 'bar'",
        "'Container' can not resolve attribute 'bar' while building 'foo'",
        "'Injector' can not resolve attribute 'bar' while building 'foo'",
    }


@attribute_error
def _t1jn9RI9v42t():
    class Container(Injector):

        foo = this.bar

    Container.foo


@attribute_error
def _yOEj1qQfsXHy():
    class Container(Injector):
        class SubContainer(Injector):

            foo = (this << 1).bar

    Container.SubContainer.foo


@attribute_error
def _vnmkIELBH3MN():
    Injector(foo=this.bar).foo


@attribute_error
def _pG9M52ZRQr2S():
    Injector(SubContainer=Injector(foo=(this << 1).bar)).SubContainer.foo


direct = CodeCollector()


@direct.parametrize
def test_deny_this_without_attribute_access(code):
    """`this` object can't be used as a dependency directly."""

    class Foo:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    message = str(exc_info.value)
    assert message == "You can not use 'this' directly in the 'Injector'"


@direct
def _b648b6f6a712(Foo):
    class Container(Injector):
        foo = Foo
        bar = this

    Container.foo


@direct
def _c147d398f4be(Foo):
    class Container(Injector):
        foo = Foo
        bar = this << 1

    Container.foo


@direct
def _a37783b6d1ad(Foo):
    Injector(foo=Foo, bar=this).foo


@direct
def _bd05271fb831(Foo):
    Injector(foo=Foo, bar=(this << 1)).foo

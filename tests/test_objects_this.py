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
        foo = Foo
        one = this.SubContainer.one
        two = this.SubContainer.two

        class SubContainer(Injector):
            one = 1
            two = 2

    foo = Container.foo
    assert isinstance(foo, Foo)
    assert foo.do() == 3


def test_attribute_getter_few_attributes():
    """We resolve attribute access until we find all specified attributes."""

    class Root:
        def __init__(self, result):
            self.result = result

    class Foo:
        def __init__(self, one):
            self.one = one

    class Container(Injector):
        root = Root
        result = this.SubContainer.foo.one

        class SubContainer(Injector):
            foo = Foo
            one = 1

    assert Container.root.result == 1


item_access = CodeCollector()


@item_access.parametrize
def test_item_getter(code):
    """We can describe item access in the `Injector` in the declarative manner."""

    class Root:
        def __init__(self, result):
            self.result = result

    result = code(Root)
    assert result == 1


@item_access
def _ce642f492941(Root):
    class Container(Injector):
        root = Root
        foo = {"one": 1}
        result = this.foo["one"]

    return Container.root.result


@item_access
def _ffa208dc1130(Root):
    class Container(Injector):
        root = Root
        foo = {"one": {"two": 1}}
        result = this.foo["one"]["two"]

    return Container.root.result


@item_access
def _e5c358190fef(Root):
    class Container(Injector):
        root = Root
        result = this.SubContainer.spam
        foo = {"bar": {"baz": 1}}

        class SubContainer(Injector):
            spam = (this << 1).foo["bar"]["baz"]

    return Container.root.result


@item_access
def _ab4cdbf60b2f(Root):
    class Container(Injector):
        root = Root
        result = this.SubContainer.SubSubContainer.spam
        foo = {"bar": {"baz": 1}}

        class SubContainer(Injector):
            class SubSubContainer(Injector):
                spam = (this << 2).foo["bar"]["baz"]

    return Container.root.result


@item_access
def _be332433b74d(Root):
    class Container(Injector):
        root = Root
        result = this.bar
        foo = [1, 2, 3]
        bar = this.foo[0]

    return Container.root.result


@item_access
def _fe150d5ebe93(Root):
    class Container(Injector):
        root = Root
        result = this.bar
        foo = {2: 1}
        bar = this.foo[2]

    return Container.root.result


@item_access
def _dc4fedcd09d8(Root):
    class Container(Injector):
        root = Root
        result = this.bar
        foo = {("x", 1): 1}
        bar = this.foo[("x", 1)]

    return Container.root.result


def test_item_getter_non_printable_key():
    """Don't use string representation as key hash function.

    We can describe item access for keys which can't be presented as normal strings.

    """

    class Root:
        def __init__(self, result):
            self.result = result

    class Boom:
        def __init__(self, salt):
            self.salt = salt

        def __hash__(self):
            return hash(self.salt)

        def __str__(self):
            return "<boom>"  # pragma: no cover

    boom = Boom("hello")

    class Container(Injector):
        root = Root
        foo = {boom: 1}
        result = this.foo[boom]

    assert Container.root.result == 1


def test_attribute_access_after_item_getter():
    """Check we can use attribute access notation after item getter notation."""

    class Root:
        def __init__(self, result):
            self.result = result

    class Baz:
        quiz = 1

    class Foo:
        bar = {"baz": Baz}

    class Container(Injector):
        root = Root
        result = this.foo.bar["baz"].quiz
        foo = Foo

    assert Container.root.result == 1


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
        "Can not resolve attribute 'bar'",
        "Can not resolve attribute 'bar' while building 'foo'",
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


deny_direct_resolve = CodeCollector()


@deny_direct_resolve.parametrize
def test_direct_this_resolve(code):
    """Attempt to resolve this directly should raise exception.

    This objects are allowed to be used as dependencies for classes.

    """
    with pytest.raises(DependencyError) as exc_info:
        code()
    expected = "'this' dependencies could only be used to instantiate classes"
    assert str(exc_info.value) == expected


@deny_direct_resolve
def _thSaFsw1po8I():
    class Container(Injector):
        a = this.b
        b = 1

    Container.a


@deny_direct_resolve
def _vIWzcvYG5qs5():
    Injector(a=this.b, b=1).a

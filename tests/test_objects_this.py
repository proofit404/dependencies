"""Tests related to the `this` object."""
from inspect import unwrap

import pytest

from collector import CodeCollector
from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError


def test_attribute_getter(define, let, has, expect):
    """We can describe attribute access in the `Injector` in declarative manner."""
    foo = define.cls(
        "Foo",
        let.fun("__init__", "self, one, two", "self.one = one", "self.two = two"),
        let.fun("do", "self", "return self.one + self.two"),
    )
    it = has(
        foo=foo,
        one="this.SubContainer.one",
        two="this.SubContainer.two",
        SubContainer=has(one="1", two="2"),
    )
    expect(it).to("isinstance(obj.foo, Foo)", "obj.foo.do() == 3")


def test_attribute_getter_few_attributes(define, let, has, expect):
    """We resolve attribute access until we find all specified attributes."""
    root = define.h("result")
    foo = define.cls("Foo", let.fun("__init__", "self, one", "self.one = one"))
    it = has(
        root=root,
        result="this.SubContainer.foo.one",
        SubContainer=has(foo=foo, one="1"),
    )
    expect(it).to("obj.root == 1")


def test_item_getter(define, let, has, expect):
    """We can describe item access in the `Injector` in the declarative manner."""
    root = define.h("result")

    it = has(root=root, result="this.foo['one']", foo="{'one': 1}")
    expect(it).to("obj.root == 1")

    it = has(root=root, result="this.foo['one']['two']", foo="{'one': {'two': 1}}")
    expect(it).to("obj.root == 1")

    it = has(
        root=root,
        result="this.SubContainer.spam",
        SubContainer=has(spam="(this << 1).foo['bar']['baz']"),
        foo="{'bar': {'baz': 1}}",
    )
    expect(it).to("obj.root == 1")

    it = has(
        root=root,
        result="this.SubContainer.SubSubContainer.spam",
        SubContainer=has(SubSubContainer=has(spam="(this << 2).foo['bar']['baz']")),
        foo="{'bar': {'baz': 1}}",
    )
    expect(it).to("obj.root == 1")

    it = has(root=root, result="this.bar", bar="this.foo[0]", foo="[1, 2, 3]")
    expect(it).to("obj.root == 1")

    it = has(root=root, result="this.bar", bar="this.foo[2]", foo="{2: 1}")
    expect(it).to("obj.root == 1")

    it = has(
        root=root, result="this.bar", foo="{('x', 1): 1}", bar="this.foo[('x', 1)]"
    )
    expect(it).to("obj.root == 1")


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


too_many = CodeCollector("stack_representation", "code")


@too_many.parametrize
def test_require_more_parents_that_injector_actually_has(stack_representation, code):
    """Verify `this` expression against depth of nesting.

    If we shift more that container levels available, we should provide meaningful
    message to user.

    """

    class Root:
        def __init__(self, foo):
            raise RuntimeError

    with pytest.raises(DependencyError) as exc_info:
        code(Root)

    expected = f"""
You tried to shift this more times than Injector has levels:

{stack_representation}
    """.strip()

    assert str(exc_info.value) == expected


@too_many(
    """
Container.root
  Container.foo
    """.strip()
)
def _s6lduD7BJpxW(Root):
    class Container(Injector):
        root = Root
        foo = (this << 1).bar

    Container.root


@too_many(
    """
Injector.root
  Injector.foo
    """.strip()
)
def _ww6xNI4YrNr6(Root):
    Injector(root=Root, foo=(this << 1).bar).root


@too_many(
    """
Container.root
  Container.foo
    Nested.foo
    """.strip()
)
def _bUICVObtDZ4I(Root):
    class Container(Injector):
        root = Root
        foo = this.Nested.foo

        class Nested(Injector):
            foo = (this << 2).bar

    Container.root


@too_many(
    """
Injector.root
  Injector.foo
    Injector.foo
    """.strip()
)
def _rN3suiVzhqMM(Root):
    Injector(root=Root, foo=this.Nested.foo, Nested=Injector(foo=(this << 2).bar)).root


attribute_error = CodeCollector("stack_representation", "code")


@attribute_error.parametrize
def test_attribute_error_on_parent_access(stack_representation, code):
    """Verify `this` object expression against existed dependencies.

    We should raise `AttributeError` if we have correct number of parents but specify
    wrong attribute name.

    """

    class Root:
        def __init__(self, foo):
            raise RuntimeError

    with pytest.raises(DependencyError) as exc_info:
        code(Root)

    expected = f"""
Can not resolve attribute 'bar':

{stack_representation}
    """.strip()

    assert str(exc_info.value) == expected


@attribute_error(
    """
Container.root
  Container.foo
    Container.bar
    """.strip()
)
def _t1jn9RI9v42t(Root):
    class Container(Injector):
        root = Root
        foo = this.bar

    Container.root


@attribute_error(
    """
Injector.root
  Injector.foo
    Injector.bar
    """.strip()
)
def _vnmkIELBH3MN(Root):
    Injector(root=Root, foo=this.bar).root


@attribute_error(
    """
Container.root
  Container.foo
    Nested.foo
      Container.bar
    """.strip()
)
def _yOEj1qQfsXHy(Root):
    class Container(Injector):
        root = Root
        foo = this.Nested.foo

        class Nested(Injector):
            foo = (this << 1).bar

    Container.root


@attribute_error(
    """
Injector.root
  Injector.foo
    Injector.foo
      Injector.bar
    """.strip()
)
def _pG9M52ZRQr2S(Root):
    Injector(root=Root, foo=this.Nested.foo, Nested=Injector(foo=(this << 1).bar)).root


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


def test_this_inspect():
    """This should not trigger inspect unwrap infinite loop."""
    assert isinstance(unwrap(this), this.__class__)

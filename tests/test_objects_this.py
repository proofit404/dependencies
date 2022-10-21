"""Tests related to the `this` object."""
from inspect import unwrap

import pytest

from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError


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


def test_item_getter():
    """We can describe item access in the `Injector` in the declarative manner."""

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        foo = {"one": 1}
        result = this.foo["one"]

    assert Container.root.result == 1


def test_item_getter1():
    """We can describe item access in the `Injector` in the declarative manner."""

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        foo = {"one": {"two": 1}}
        result = this.foo["one"]["two"]

    assert Container.root.result == 1


def test_item_getter2():
    """We can describe item access in the `Injector` in the declarative manner."""

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        result = this.SubContainer.spam
        foo = {"bar": {"baz": 1}}

        class SubContainer(Injector):
            spam = (this << 1).foo["bar"]["baz"]

    assert Container.root.result == 1


def test_item_getter3():
    """We can describe item access in the `Injector` in the declarative manner."""

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        result = this.SubContainer.SubSubContainer.spam
        foo = {"bar": {"baz": 1}}

        class SubContainer(Injector):
            class SubSubContainer(Injector):
                spam = (this << 2).foo["bar"]["baz"]

    assert Container.root.result == 1


def test_item_getter4():
    """We can describe item access in the `Injector` in the declarative manner."""

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        result = this.bar
        foo = [1, 2, 3]
        bar = this.foo[0]

    assert Container.root.result == 1


def test_item_getter5():
    """We can describe item access in the `Injector` in the declarative manner."""

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        result = this.bar
        foo = {2: 1}
        bar = this.foo[2]

    assert Container.root.result == 1


def test_item_getter6():
    """We can describe item access in the `Injector` in the declarative manner."""

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        result = this.bar
        foo = {("x", 1): 1}
        bar = this.foo[("x", 1)]

    assert Container.root.result == 1


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


def test_this_deny_negative_integers():
    """We can't shift `this` with negative integer."""
    with pytest.raises(ValueError, match=".*") as exc_info:
        this << -1

    assert str(exc_info.value) == "Positive integer argument is required"

    with pytest.raises(ValueError, match=".*") as exc_info:
        this << 0

    assert str(exc_info.value) == "Positive integer argument is required"


def test_require_more_parents_that_injector_actually_has():
    """Verify `this` expression against depth of nesting.

    If we shift more that container levels available, we should provide meaningful
    message to user.

    """

    class Root:
        def __init__(self, foo):
            raise RuntimeError

    class Container(Injector):
        root = Root
        foo = (this << 1).bar

    with pytest.raises(DependencyError) as exc_info:
        Container.root

    expected = """
You tried to shift this more times than Injector has levels:

Container.root
  Container.foo
    """.strip()

    assert str(exc_info.value) == expected


def test_require_more_parents_that_injector_actually_has1():
    """Verify `this` expression against depth of nesting.

    If we shift more that container levels available, we should provide meaningful
    message to user.

    """

    class Root:
        def __init__(self, foo):
            raise RuntimeError

    class Container(Injector):
        root = Root
        foo = this.Nested.foo

        class Nested(Injector):
            foo = (this << 2).bar

    with pytest.raises(DependencyError) as exc_info:
        Container.root

    expected = """
You tried to shift this more times than Injector has levels:

Container.root
  Container.foo
    Nested.foo
    """.strip()

    assert str(exc_info.value) == expected


def test_attribute_error_on_parent_access():
    """Verify `this` object expression against existed dependencies.

    We should raise `AttributeError` if we have correct number of parents but specify
    wrong attribute name.

    """

    class Root:
        def __init__(self, foo):
            raise RuntimeError

    class Container(Injector):
        root = Root
        foo = this.bar

    with pytest.raises(DependencyError) as exc_info:
        Container.root

    expected = """
Can not resolve attribute 'bar':

Container.root
  Container.foo
    Container.bar
    """.strip()

    assert str(exc_info.value) == expected


def test_attribute_error_on_parent_access1():
    """Verify `this` object expression against existed dependencies.

    We should raise `AttributeError` if we have correct number of parents but specify
    wrong attribute name.

    """

    class Root:
        def __init__(self, foo):
            raise RuntimeError

    class Container(Injector):
        root = Root
        foo = this.Nested.foo

        class Nested(Injector):
            foo = (this << 1).bar

    with pytest.raises(DependencyError) as exc_info:
        Container.root

    expected = """
Can not resolve attribute 'bar':

Container.root
  Container.foo
    Nested.foo
      Container.bar
    """.strip()

    assert str(exc_info.value) == expected


@pytest.mark.parametrize("Bar", [this, this << 1])
def test_deny_this_without_attribute_access(Bar):
    """`this` object can't be used as a dependency directly."""

    class Foo:
        pass

    class Container(Injector):
        foo = Foo
        bar = Bar

    with pytest.raises(DependencyError) as exc_info:
        Container.foo

    expected = "You can not use 'this' directly in the 'Injector'"

    assert str(exc_info.value) == expected


def test_this_inspect():
    """This should not trigger inspect unwrap infinite loop."""
    assert isinstance(unwrap(this), this.__class__)

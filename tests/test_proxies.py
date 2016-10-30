from textwrap import dedent

import pytest

from dependencies import Injector, this, DependencyError


# Declarative attribute access.


def test_attribute_getter():
    """
    We can describe attribute access in the `Injector` in declarative
    manner.
    """

    class Foo(object):
        def __init__(self, one, two):
            self.one = one
            self.two = two
        def do(self):  # noqa: E301
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
    """
    We resolve attribute access until we find all specified
    attributes.
    """

    class Foo(object):
        def __init__(self, one):
            self.one = one

    class Container(Injector):
        class SubContainer(Injector):
            foo = Foo
            one = 1
        foo = this.SubContainer.foo.one

    assert Container.foo == 1


# Parent attribute access.


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Container(Injector):
        foo = 1

        class SubContainer(Injector):
            bar = (this << 1).foo
    """,
    # Let notation.
    """
    class OuterContainer(Injector):
        foo = 1

    class SubContainer(Injector):
        bar = (this << 1).foo

    Container = OuterContainer.let(SubContainer=SubContainer)
    """,
    # Attribute assignment.
    """
    class Container(Injector):
        foo = 1

    class SubContainer(Injector):
        bar = (this << 1).foo

    Container.SubContainer = SubContainer
    """,
    # Use decorator.
    """
    class Container(Injector):
        foo = 1

    @Container.use
    class SubContainer(Injector):
        bar = (this << 1).foo
    """,
])
def test_attribute_getter_parent_access(code):
    """We can access attribute of outer container."""

    scope = {'Injector': Injector, 'this': this}
    exec(dedent(code), scope)
    Container = scope['Container']
    assert Container.SubContainer.bar == 1


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Container(Injector):
        foo = 1

        class SubContainer(Injector):

            class SubSubContainer(Injector):
                bar = (this << 2).foo
    """,
    # Let notation.
    """
    class OuterContainer(Injector):
        foo = 1

    class SubContainer(Injector):

        class SubSubContainer(Injector):
            bar = (this << 2).foo

    Container = OuterContainer.let(SubContainer=SubContainer)
    """,
    # Attribute assignment.
    """
    class Container(Injector):
        foo = 1

        class SubContainer(Injector):
            pass

    class SubSubContainer(Injector):
        bar = (this << 2).foo

    Container.SubContainer.SubSubContainer = SubSubContainer
    """,
    # Use decorator.
    """
    class Container(Injector):
        foo = 1

        class SubContainer(Injector):
            pass

    @Container.SubContainer.use
    class SubSubContainer(Injector):
        bar = (this << 2).foo
    """,
])
def test_attribute_getter_few_parents(code):
    """We can access attribute of outer container in any nesting depth."""

    scope = {'Injector': Injector, 'this': this}
    exec(dedent(code), scope)
    Container = scope['Container']
    assert Container.SubContainer.SubSubContainer.bar == 1


# Declarative item access.


@pytest.mark.parametrize('code', [
    # Get item with string key.
    """
    class Container(Injector):
        foo = {'one': 1}
        one = this.foo['one']

    result = Container.one
    """,
    # Get items as many times as we want.
    """
    class Container(Injector):
        foo = {'one': {'two': 1}}
        two = this.foo['one']['two']

    result = Container.two
    """,
    # Get item from the outer container.
    """
    class Container(Injector):
        foo = {'bar': {'baz': 1}}

        class SubContainer(Injector):
            spam = (this << 1).foo['bar']['baz']

    result = Container.SubContainer.spam
    """,
    # Get item from the outer container of any depth level.
    """
    class Container(Injector):
        foo = {'bar': {'baz': 1}}

        class SubContainer(Injector):

            class SubSubContainer(Injector):
                spam = (this << 2).foo['bar']['baz']

    result = Container.SubContainer.SubSubContainer.spam
    """,
    # Get items from list.
    """
    class Container(Injector):
        foo = [1, 2, 3]
        bar = this.foo[0]

    result = Container.bar
    """,
    # Get items from dict with digit keys.
    """
    class Container(Injector):
        foo = {2: 1}
        bar = this.foo[2]

    result = Container.bar
    """,
    # Get items from dict with tuple keys.
    """
    class Container(Injector):
        foo = {('x', 1): 1}
        bar = this.foo[('x', 1)]

    result = Container.bar
    """,
])
def test_item_getter(code):
    """
    We can describe item access in the `Injector` in the
    declarative manner.
    """

    scope = {'Injector': Injector, 'this': this}
    exec(dedent(code), scope)
    result = scope['result']
    assert result == 1


def test_item_getter_non_printable_key():
    """
    We can describe item access for keys which can't be presented as
    normal strings.
    """

    class Boom(object):
        def __init__(self, salt):
            self.salt = salt
        def __hash__(self):     # noqa: E301
            return hash(self.salt)
        def __str__(self):      # noqa: E301
            return "<boom>"

    boom = Boom('hello')

    class Container(Injector):
        foo = {boom: 1}
        bar = this.foo[boom]

    assert Container.bar == 1


# Docstrings.


def test_docstrings():
    """Check we can access all API entry points documentation."""

    assert this.__doc__ == (
        'Declare attribute and item access during dependency injection.'
    )


# Deny direct this proxy usage.


@pytest.mark.xfail              # FIXME: support declared behavior
@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Container(Injector):
        foo = this
    """,
    # Declarative injector with parent access.
    """
    class Container(Injector):
        foo = (this << 1)
    """,
    # Let notation.
    """
    Injector.let(foo=this)
    """,
    # Let notation with parent access.
    """
    Injector.let(foo=(this << 1))
    """,
    # Attribute assignment.
    """
    class Container(Injector):
        pass

    Container.foo = this
    """,
    # Attribute assignment with parent access.
    """
    class Container(Injector):
        pass

    Container.foo = (this << 1)
    """,
    # TODO: Maybe deny injection of `this` subclasses.
    #
    # Use decorator.
    # """""",
    #
    # Use decorator with parent.
    # """""",
])
def test_attribute_getter_arguments_validation(code):
    """TODO: write doc and proper test name"""

    scope = {'Injector': Injector, 'this': this}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    message = str(exc_info.value)
    assert message == "You can not use 'this' directly in the 'Injector'"


# TODO: minimize test number here.
#
# FIXME: same SubContainer for different parents should work.
#
# FIXME: add deeper dict example.
#
# For now we use separate item and attribute access.  With this
# approach it isn't possible to take items from attributes like that:
#
# class Container(Injector):
#     class Foo(object):
#         bar = {'baz': 1}
#     baz = item('Foo', 'bar', 'baz')
#
# `Container.baz` will give us TypeError: 'Foo' object is not subscriptable
#
# TODO: test `this` against negative numbers and non digits

from textwrap import dedent

import pytest

from dependencies import Injector, attribute, item, DependencyError


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
        foo = attribute('SubContainer', 'foo')

    foo = Container.foo
    assert isinstance(foo, Foo)
    assert foo.do() == 3


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Container(Injector):
        foo = 1

        class SubContainer(Injector):
            bar = attribute('..', 'foo')
    """,
    # Let notation.
    """
    class OuterContainer(Injector):
        foo = 1

    class SubContainer(Injector):
        bar = attribute('..', 'foo')

    Container = OuterContainer.let(SubContainer=SubContainer)
    """,
    # Attribute assignment.
    """
    class Container(Injector):
        foo = 1

    class SubContainer(Injector):
        bar = attribute('..', 'foo')

    Container.SubContainer = SubContainer
    """,
    # Use decorator.
    """
    class Container(Injector):
        foo = 1

    @Container.use
    class SubContainer(Injector):
        bar = attribute('..', 'foo')
    """,
])
def test_attribute_getter_parent_access(code):
    """We can access attribute of outer container."""

    scope = {'Injector': Injector, 'attribute': attribute}
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
                bar = attribute('..', '..', 'foo')
    """,
    # Let notation.
    """
    class OuterContainer(Injector):
        foo = 1

    class SubContainer(Injector):

        class SubSubContainer(Injector):
            bar = attribute('..', '..', 'foo')

    Container = OuterContainer.let(SubContainer=SubContainer)
    """,
    # Attribute assignment.
    """
    class Container(Injector):
        foo = 1

        class SubContainer(Injector):
            pass

    class SubSubContainer(Injector):
        bar = attribute('..', '..', 'foo')

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
        bar = attribute('..', '..', 'foo')
    """,
])
def test_attribute_getter_few_parents(code):
    """We can access attribute of outer container in any nesting depth."""

    scope = {'Injector': Injector, 'attribute': attribute}
    exec(dedent(code), scope)
    Container = scope['Container']
    assert Container.SubContainer.SubSubContainer.bar == 1


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
        foo = attribute('SubContainer', 'foo', 'one')

    assert Container.foo == 1


@pytest.mark.parametrize('args, error, error_type', [
    ([], "'attrs' argument can not be empty", DependencyError),
    (['1x'], "'1x' is invalid attribute name", DependencyError),
    ([1], "attribute name should be a string", TypeError),
])
def test_attribute_getter_arguments_validation(args, error, error_type):
    """Check `attribute` proxy against different incorrect inputs."""

    with pytest.raises(error_type) as exc_info:
        attribute(*args)

    message = str(exc_info.value)
    assert message == error


# Declarative item access.


@pytest.mark.parametrize('code', [
    # Get item with string key.
    """
    class Container(Injector):
        foo = {'one': 1}
        one = item('foo', 'one')

    result = Container.one
    """,
    # Get items as many times as we want.
    """
    class Container(Injector):
        foo = {'one': {'two': 1}}
        two = item('foo', 'one', 'two')

    result = Container.two
    """,
    # Get item from the outer container.
    """
    class Container(Injector):
        foo = {'bar': {'baz': 1}}

        class SubContainer(Injector):
            spam = item('..', 'foo', 'bar', 'baz')

    result = Container.SubContainer.spam
    """,
    # Get item from the outer container of any depth level.
    """
    class Container(Injector):
        foo = {'bar': {'baz': 1}}

        class SubContainer(Injector):

            class SubSubContainer(Injector):
                spam = item('..', '..', 'foo', 'bar', 'baz')

    result = Container.SubContainer.SubSubContainer.spam
    """,
    # Get items from list.
    """
    class Container(Injector):
        foo = [1, 2, 3]
        bar = item('foo', 0)

    result = Container.bar
    """,
    # Get items from dict with digit keys.
    """
    class Container(Injector):
        foo = {2: 1}
        bar = item('foo', 2)

    result = Container.bar
    """,
    # Get items from dict with tuple keys.
    """
    class Container(Injector):
        foo = {('x', 1): 1}
        bar = item('foo', ('x', 1))

    result = Container.bar
    """,
])
def test_item_getter(code):
    """
    We can describe item access in the `Injector` in the
    declarative manner.
    """

    scope = {'Injector': Injector, 'item': item}
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
        bar = item('foo', boom)

    assert Container.bar == 1


@pytest.mark.parametrize('args, error', [
    ([], "'items' argument can not be empty"),
    (['foo'], "'items' argument can not be empty"),
    (['..', 'foo'], "'items' argument can not be empty"),
    (['1x', 'foo'], "'1x' is invalid attribute name"),
])
def test_item_getter_arguments_validation(args, error):
    """Check `attribute` proxy against different incorrect inputs."""

    with pytest.raises(DependencyError) as exc_info:
        item(*args)

    message = str(exc_info.value)
    assert message == error


# Docstrings.


def test_docstrings():
    """Check we can access all API entry points documentation."""

    assert attribute.__doc__ == (
        'Declare attribute access during dependency injection.'
    )
    assert item.__doc__ == (
        'Declare item access during dependency injection.'
    )

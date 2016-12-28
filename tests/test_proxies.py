import pytest
from helpers import CodeCollector

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


parent_attr = CodeCollector()


@parent_attr.parametrize
def test_attribute_getter_parent_access(code):
    """We can access attribute of outer container."""

    Container = code()
    assert Container.SubContainer.bar == 1


@parent_attr
def ac7814095628():
    """Declarative injector."""

    class Container(Injector):
        foo = 1

        class SubContainer(Injector):
            bar = (this << 1).foo

    return Container


@parent_attr
def f607abc82079():
    """Let notation."""

    class OuterContainer(Injector):
        foo = 1

    class SubContainer(Injector):
        bar = (this << 1).foo

    Container = OuterContainer.let(SubContainer=SubContainer)

    return Container


@parent_attr
def f2bfa4318b60():
    """Attribute assignment."""

    class Container(Injector):
        foo = 1

    class SubContainer(Injector):
        bar = (this << 1).foo

    Container.SubContainer = SubContainer

    return Container


@parent_attr
def ba9b64d1fed9():
    """Use decorator."""

    class Container(Injector):
        foo = 1

    @Container.use
    class SubContainer(Injector):
        bar = (this << 1).foo

    return Container


few_parent_attr = CodeCollector()


@pytest.mark.xfail
@few_parent_attr.parametrize
def test_attribute_getter_few_parents(code):
    """We can access attribute of outer container in any nesting depth."""

    Container = code()
    assert Container.SubContainer.SubSubContainer.bar == 1


@few_parent_attr
def e477afc961b6():
    """Declarative injector."""

    class Container(Injector):
        foo = 1

        class SubContainer(Injector):

            class SubSubContainer(Injector):
                bar = (this << 2).foo

    return Container


@few_parent_attr
def c4ed4c61e154():
    """Let notation."""

    class OuterContainer(Injector):
        foo = 1

    class SubContainer(Injector):

        class SubSubContainer(Injector):
            bar = (this << 2).foo

    Container = OuterContainer.let(SubContainer=SubContainer)

    return Container


@few_parent_attr
def fc04e2ab714b():
    """Attribute assignment."""

    class Container(Injector):
        foo = 1

        class SubContainer(Injector):
            pass

    class SubSubContainer(Injector):
        bar = (this << 2).foo

    Container.SubContainer.SubSubContainer = SubSubContainer

    return Container


@few_parent_attr
def ecd27596248a():
    """Use decorator."""

    class Container(Injector):
        foo = 1

        class SubContainer(Injector):
            pass

    @Container.SubContainer.use
    class SubSubContainer(Injector):
        bar = (this << 2).foo

    return Container


def test_one_subcontainer_multiple_parents():
    """
    Same sub container can be used in many parent containers.  This
    usage should not overlap those containers.
    """

    class SubContainer(Injector):
        foo = (this << 1).foo

    class Container1(Injector):
        foo = 1
        sub = SubContainer

    class Container2(Injector):
        foo = 2
        sub = SubContainer

    assert Container1.sub.foo == 1
    assert Container2.sub.foo == 2


item_access = CodeCollector()


@pytest.mark.xfail
@item_access.parametrize
def test_item_getter(code):
    """
    We can describe item access in the `Injector` in the
    declarative manner.
    """

    result = code()
    assert result == 1


@item_access
def ce642f492941():
    """Get item with string key."""

    class Container(Injector):
        foo = {'one': 1}
        one = this.foo['one']

    result = Container.one

    return result


@item_access
def ffa208dc1130():
    """Get items as many times as we want."""

    class Container(Injector):
        foo = {'one': {'two': 1}}
        two = this.foo['one']['two']

    result = Container.two

    return result


@item_access
def e5c358190fef():
    """Get item from the outer container."""

    class Container(Injector):
        foo = {'bar': {'baz': 1}}

        class SubContainer(Injector):
            spam = (this << 1).foo['bar']['baz']

    result = Container.SubContainer.spam

    return result


@item_access
def ab4cdbf60b2f():
    """Get item from the outer container of any depth level."""

    class Container(Injector):
        foo = {'bar': {'baz': 1}}

        class SubContainer(Injector):

            class SubSubContainer(Injector):
                spam = (this << 2).foo['bar']['baz']

    result = Container.SubContainer.SubSubContainer.spam

    return result


@item_access
def be332433b74d():
    """Get items from list."""

    class Container(Injector):
        foo = [1, 2, 3]
        bar = this.foo[0]

    result = Container.bar

    return result


@item_access
def fe150d5ebe93():
    """Get items from dict with digit keys."""

    class Container(Injector):
        foo = {2: 1}
        bar = this.foo[2]

    result = Container.bar

    return result


@item_access
def dc4fedcd09d8():
    """Get items from dict with tuple keys."""

    class Container(Injector):
        foo = {('x', 1): 1}
        bar = this.foo[('x', 1)]

    result = Container.bar

    return result


def test_item_getter_non_printable_key():
    """
    We can describe item access for keys which can't be presented as
    normal strings.
    """

    class Boom(object):

        def __init__(self, salt):
            self.salt = salt

        def __hash__(self):
            return hash(self.salt)

        def __str__(self):
            return "<boom>"

    boom = Boom('hello')

    class Container(Injector):
        foo = {boom: 1}
        bar = this.foo[boom]

    assert Container.bar == 1


def test_docstrings():
    """Check we can access all API entry points documentation."""

    assert this.__doc__ == (
        'Declare attribute and item access during dependency injection.')


direct_proxy = CodeCollector()


@direct_proxy.parametrize
def test_attribute_getter_arguments_validation(code):
    """TODO: write doc and proper test name"""

    with pytest.raises(DependencyError) as exc_info:
        code()

    message = str(exc_info.value)
    assert message == "You can not use 'this' directly in the 'Injector'"


@direct_proxy
def b648b6f6a712():
    """Declarative injector."""

    class Container(Injector):
        foo = this


@direct_proxy
def c147d398f4be():
    """Declarative injector with parent access."""

    class Container(Injector):
        foo = (this << 1)


@direct_proxy
def a37783b6d1ad():
    """Let notation."""

    Injector.let(foo=this)


@direct_proxy
def bd05271fb831():
    """Let notation with parent access."""

    Injector.let(foo=(this << 1))


@direct_proxy
def f44e0a7db9a2():
    """Attribute assignment."""

    class Container(Injector):
        pass

    Container.foo = this


@direct_proxy
def a3849bbb3105():
    """Attribute assignment with parent access."""

    class Container(Injector):
        pass

    Container.foo = (this << 1)


# TODO: minimize test number here.
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
#
# TODO: what if we shift more that container levels available?  What
# we should do in this case?

"""Tests related to Injector classes written inside other Injector classes."""
import pytest

from dependencies import Injector
from dependencies import Package
from dependencies import this
from helpers import CodeCollector


pytestmark = pytest.mark.xfail

parent_attr = CodeCollector()
subcontainer = CodeCollector("sub")


@parent_attr.parametrize
@subcontainer.parametrize
def test_attribute_getter_parent_access(code, sub):
    """We can access attribute of outer container."""
    Container = code(sub())
    assert Container.SubContainer.bar == 1


@parent_attr
def _ac7814095628(sub):
    class Container(Injector):
        foo = 1
        SubContainer = sub

    return Container


@parent_attr
def _f607abc82079(sub):
    return Injector(foo=1, SubContainer=sub)


@subcontainer
def _iGphUpthTooT():
    class SubContainer(Injector):
        bar = (this << 1).foo

    return SubContainer


@subcontainer
def _nurKbeeqoNCn():
    return Injector(bar=(this << 1).foo)


@subcontainer
def _hHytjZxQjNPQ():
    examples = Package("examples")

    return examples.injected.SubContainer


few_parent_attr = CodeCollector()
middle_container = CodeCollector("middle")
lowest_container = CodeCollector("lowest")


@few_parent_attr.parametrize
@middle_container.parametrize
@lowest_container.parametrize
def test_attribute_getter_few_parents(code, middle, lowest):
    """We can access attribute of outer container in any nesting depth."""
    Container = code(middle(lowest()))
    assert Container.SubContainer.SubSubContainer.bar == 1


@few_parent_attr
def _e477afc961b6(middle):
    class Container(Injector):
        foo = 1
        SubContainer = middle

    return Container


@few_parent_attr
def _c4ed4c61e154(middle):
    return Injector(foo=1, SubContainer=middle)


@middle_container
def _hjVHyztckQNe(lowest):
    class SubContainer(Injector):
        SubSubContainer = lowest

    return SubContainer


@middle_container
def _gYijGKMqAbZN(lowest):
    return Injector(SubSubContainer=lowest)


@lowest_container
def _pDqnxaJFVRcS():
    class SubSubContainer(Injector):
        bar = (this << 2).foo

    return SubSubContainer


@lowest_container
def _heSHjuBBFVLp():
    return Injector(bar=(this << 2).foo)


@lowest_container
def _mVVyoyBmvQwc():
    examples = Package("examples")

    return examples.injected.SubSubContainer


def test_one_subcontainer_multiple_parents():
    """Same sub container can be used in many parent containers.

    This usage should not overlap those containers.

    """

    class SubContainer(Injector):
        bar = (this << 1).foo

    class Container1(Injector):
        foo = 1
        sub = SubContainer

    class Container2(Injector):
        foo = 2
        sub = SubContainer

    assert Container1.sub.bar == 1
    assert Container2.sub.bar == 2  # pragma: no cover

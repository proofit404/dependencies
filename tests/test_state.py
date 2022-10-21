"""Tests related to the injection process state."""
import pytest

from dependencies import Injector
from dependencies import this
from dependencies import value


def test_evaluate_once_different_types(A, B, C, D, times):
    """Evaluate each node in the dependencies graph once.

    Arguments of dependencies of different types should be evaluated once. This rules
    applies to classes and @value objects. This is a variation of the test above written
    against all necessary inputs.

    """

    class Root:
        def __init__(self, a):
            self.a = a

    class Container(Injector):
        root = Root
        a = A
        b = B
        c = C
        d = D

    assert sum(times) == 0
    Container.root.a
    assert sum(times) == 1


def _evaluate_once_a():
    class A:
        def __init__(self, b, c):
            pass

    @value
    def a(b, c):
        pass

    yield A
    yield a
    # NOTE: Package is missing.


@pytest.fixture(params=_evaluate_once_a())
def A(request):
    """All possible definitions."""
    return request.param


def _evaluate_once_b():
    class B:
        def __init__(self, d):
            pass

    @value
    def b(d):
        pass

    yield B
    yield b
    # NOTE: Package is missing.


@pytest.fixture(params=_evaluate_once_b())
def B(request):
    """All possible definitions."""
    return request.param


def _evaluate_once_c():
    class C:
        def __init__(self, d):
            pass

    @value
    def c(d):
        pass

    yield C
    yield c
    # NOTE: Package is missing.


@pytest.fixture(params=_evaluate_once_c())
def C(request):
    """All possible definitions."""
    return request.param


def _evaluate_once_d_class(times):
    class D:
        def __init__(self):
            times.append(1)

    return D


def _evaluate_once_d_value(times):
    @value
    def d():
        times.append(1)

    return d


@pytest.fixture(params=[_evaluate_once_d_class, _evaluate_once_d_value])
def D(request, times):
    """All possible definitions."""
    return request.param(times)
    # NOTE: Package is missing.


@pytest.fixture()
def times():
    """Count number of times object was built."""
    return []


def test_evaluate_once_nested_container(An, Bn, Cn, Dn, En, d_times, e_times):
    """Evaluate each node in the dependencies graph once.

    This example focus on evaluating dependencies once when they do spread between
    different levels of nesting and point into each other with `this` expression.

    """

    class Root:
        def __init__(self, a):
            self.a = a

    class Container(Injector):
        root = Root
        a = An
        b = this.Nested.b
        d = this.Nested.d
        e = En

        class Nested(Injector):
            b = Bn
            c = this.Nested.c
            d = this.Nested.d
            e = (this << 1).e

            class Nested(Injector):
                c = Cn
                d = this.Nested.d
                e = (this << 2).e

                class Nested(Injector):
                    d = Dn
                    e = (this << 3).e

    assert sum(d_times) == 0
    assert sum(e_times) == 0
    Container.root.a
    assert sum(d_times) == 1
    assert sum(e_times) == 1


def _evaluate_once_nested_a():
    class A:
        def __init__(self, b, d, e):
            pass

    @value
    def a(b, d, e):
        pass

    yield A
    yield a


@pytest.fixture(params=_evaluate_once_nested_a())
def An(request):
    """All possible definitions."""
    return request.param


def _evaluate_once_nested_b():
    class B:
        def __init__(self, c, d, e):
            pass

    @value
    def b(c, d, e):
        pass

    yield B
    yield b


@pytest.fixture(params=_evaluate_once_nested_b())
def Bn(request):
    """All possible definitions."""
    return request.param


def _evaluate_once_nested_c():
    class C:
        def __init__(self, d, e):
            pass

    @value
    def c(d, e):
        pass

    yield C
    yield c


@pytest.fixture(params=_evaluate_once_nested_c())
def Cn(request):
    """All possible definitions."""
    return request.param


def _evaluate_once_nested_d_class(times):
    class D:
        def __init__(self, e):
            times.append(1)

    return D


def _evaluate_once_nested_d_value(times):
    @value
    def d(e):
        times.append(1)

    return d


@pytest.fixture(params=[_evaluate_once_nested_d_class, _evaluate_once_nested_d_value])
def Dn(request, d_times):
    """All possible definitions."""
    return request.param(d_times)
    # NOTE: Package is missing.


def _evaluate_once_nested_e_class(times):
    class E:
        def __init__(self):
            times.append(1)

    return E


def _evaluate_once_nested_e_value(times):
    @value
    def e():
        times.append(1)

    return e


@pytest.fixture(params=[_evaluate_once_nested_e_class, _evaluate_once_nested_e_value])
def En(request, e_times):
    """All possible definitions."""
    return request.param(e_times)
    # NOTE: Package is missing.


@pytest.fixture()
def d_times():
    """Count number of times object was built."""
    return []


@pytest.fixture()
def e_times():
    """Count number of times object was built."""
    return []

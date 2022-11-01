"""Tests related to the injection process state."""
import pytest

from dependencies import Injector
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


@pytest.fixture()
def times():
    """Count number of times object was built."""
    return []

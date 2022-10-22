"""Tests related to the injection process state."""
import pytest

from dependencies import Injector
from dependencies import value
from signature import Signature


def _evaluate_once_a():
    class A:
        def __init__(self, b, c):
            self.b = b
            self.c = c

    @value
    def a(b, c):
        return Signature(b=b, c=c)

    yield A
    yield a


def _evaluate_once_b():
    class B:
        def __init__(self, d):
            self.d = d

    @value
    def b(d):
        return Signature(d=d)

    yield B
    yield b


def _evaluate_once_c():
    class C:
        def __init__(self, d):
            self.d = d

    @value
    def c(d):
        return Signature(d=d)

    yield C
    yield c


def _evaluate_once_d():
    class D:
        def __init__(self):
            pass

    @value
    def d():
        return object()

    yield D
    yield d


@pytest.mark.parametrize("A", _evaluate_once_a())
@pytest.mark.parametrize("B", _evaluate_once_b())
@pytest.mark.parametrize("C", _evaluate_once_c())
@pytest.mark.parametrize("D", _evaluate_once_d())
def test_evaluate_once(e, expect, A, B, C, D):
    """Evaluate each node in the dependencies graph once."""
    expect.skip_if_scope()

    class Container(Injector):
        v = e.Take["a"]
        a = A
        b = B
        c = C
        d = D

    @expect(Container)
    def case(it):
        assert it.v.b.d is not it.v.b.d
        assert it.v.b.d is not it.v.c.d
        v = it.v
        assert v.b.d is v.c.d

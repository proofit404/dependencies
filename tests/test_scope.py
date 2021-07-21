"""Tests related to scope object."""
from dependencies import Injector
from dependencies import this
from helpers import CodeCollector


hide_scope_attributes = CodeCollector()


@hide_scope_attributes.parametrize
def test_hide_scope_attributes(code):
    """Check attributes protection.

    Scope object own attributes like graph and cache should not be awailable to the
    library user.

    """

    class Result:
        def __init__(self, graph, cache):
            self.graph = graph
            self.cache = cache

    result = code(Result)
    assert result.graph == 1
    assert result.cache == 2


@hide_scope_attributes
def _i8d3DAfwAGTJ(Result):
    class Container(Injector):
        result = Result
        graph = this.Nested.graph
        cache = this.Nested.cache

        class Nested(Injector):
            graph = 1
            cache = 2

    return Container.result


@hide_scope_attributes
def _a1Jv3seOJb6U(Result):
    return Injector(
        result=Result,
        graph=this.Nested.graph,
        cache=this.Nested.cache,
        Nested=Injector(graph=1, cache=2),
    ).result

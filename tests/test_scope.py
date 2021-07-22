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


sticky_scope = CodeCollector()


@sticky_scope.parametrize
def test_sticky_scope(code):
    """Check sticky scope implementation.

    All objects instantiated during sticky scope life-time should be instantiated once.
    That way we would be able to access inner structures of high-level instancies which
    may protect their inner state (which is a good thing).

    """

    class App:
        def __init__(self, db):
            self.db = db

    class DB:
        pass

    Container = code(App, DB)
    with Container as container:
        app = container.app
        db = container.db
    assert app.db is db


@sticky_scope
def _wz3C9jpJjT4A(App, DB):
    class Container(Injector):
        app = App
        db = DB

    return Container


@sticky_scope
def _a2w333ZI7L0a(App, DB):
    return Injector(app=App, db=DB)

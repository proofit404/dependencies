"""Tests related to setup and teardown of @value decorator."""
from collector import CodeCollector
from dependencies import Injector
from dependencies import value


setup_and_teardown = CodeCollector()


@setup_and_teardown.parametrize
def test_setup_and_teardown_value(code):
    """@value could decorate a generator function."""

    class App:
        def __init__(self, lock):
            assert isinstance(lock, Lock)
            assert lock.resource == "/"

    class Lock:
        def __init__(self, resource):
            self.resource = resource

        def acquire(self):
            result.append("setup")

        def release(self):
            result.append("teardown")

    result = []
    Container = code(App, Lock)
    with Container as container:
        assert result == ["setup"]
        container.app
    assert result == ["setup", "teardown"]


@setup_and_teardown
def _u5GLvAblXmz1(App, Lock):
    class Container(Injector):
        app = App
        resource = "/"

        @value
        def lock(resource):
            instance = Lock(resource)
            instance.acquire()
            yield instance
            instance.release()

    return Container


@setup_and_teardown
def _imvsnuRtTGOL(App, Lock):
    @value
    def lock(resource):
        instance = Lock(resource)
        instance.acquire()
        yield instance
        instance.release()

    return Injector(app=App, lock=lock, resource="/")


setup_and_teardown_order = CodeCollector()


@setup_and_teardown_order.parametrize
def test_setup_and_teardown_execution_order(code):
    """Validate execution order of @value object steps.

    Order of exectution for teardown steps should be an opposite to the order for setup
    steps taken.

    """

    class App:
        def __init__(self, foo):
            ...

    class Lock:
        def __init__(self, name):
            self.name = name

        def acquire(self):
            result.append(f"setup {self.name}")

        def release(self):
            result.append(f"teardown {self.name}")

    result = []
    Container = code(App, Lock)
    with Container as container:
        assert result == ["setup a", "setup b", "setup c"]
        container.app
    assert result == [
        "setup a",
        "setup b",
        "setup c",
        "teardown c",
        "teardown b",
        "teardown a",
    ]


@setup_and_teardown_order
def _zHnU48Yd7E9z(App, Lock):
    class Container(Injector):
        app = App

        @value
        def foo(bar):
            instance = Lock("c")
            instance.acquire()
            yield instance
            instance.release()

        @value
        def bar(baz):
            instance = Lock("b")
            instance.acquire()
            yield instance
            instance.release()

        @value
        def baz():
            instance = Lock("a")
            instance.acquire()
            yield instance
            instance.release()

    return Container


@setup_and_teardown_order
def _pzXX2c1pFGT8(App, Lock):
    @value
    def foo(bar):
        instance = Lock("c")
        instance.acquire()
        yield instance
        instance.release()

    @value
    def bar(baz):
        instance = Lock("b")
        instance.acquire()
        yield instance
        instance.release()

    @value
    def baz():
        instance = Lock("a")
        instance.acquire()
        yield instance
        instance.release()

    return Injector(app=App, foo=foo, bar=bar, baz=baz)

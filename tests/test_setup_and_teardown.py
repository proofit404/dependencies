"""Tests related to setup and teardown of @value decorator."""
from dependencies import Injector
from dependencies import value


def test_setup_and_teardown_value():
    """@value could decorate a generator function."""
    result = []

    class App:
        def __init__(self, lock):
            self.lock = lock

    class Lock:
        def __init__(self, resource):
            self.resource = resource

        def acquire(self):
            result.append("setup")

        def release(self):
            result.append("teardown")

    class Container(Injector):
        app = App
        resource = "/"

        @value
        def lock(resource):
            instance = Lock(resource)
            instance.acquire()
            yield instance
            instance.release()

    with Container as container:
        assert result == ["setup"]
        assert isinstance(container.app.lock, Lock)
        assert container.app.lock.resource == "/"

    assert result == ["setup", "teardown"]


def test_setup_and_teardown_execution_order():
    """Validate execution order of @value object steps.

    Order of exectution for teardown steps should be an opposite to the order for setup
    steps taken.

    """
    result = []

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

    with Container as container:
        assert result == ["setup a", "setup b", "setup c"]
        assert isinstance(container.app, App)

    assert result == [
        "setup a",
        "setup b",
        "setup c",
        "teardown c",
        "teardown b",
        "teardown a",
    ]

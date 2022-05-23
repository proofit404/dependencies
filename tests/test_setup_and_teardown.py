"""Tests related to setup and teardown of @value decorator."""
from dependencies import Injector
from dependencies import value
from helpers import CodeCollector


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

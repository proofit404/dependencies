import pytest

from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


celery = pytest.importorskip("celery")
contrib = pytest.importorskip("dependencies.contrib.celery")


@pytest.fixture()
def celery_app():
    """Simulate global Celery application instance."""

    app = celery.Celery()
    app.conf.update(task_always_eager=True, task_eager_propagates=True)
    app.tasks.clear()
    return app


class Run(object):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        assert self.args == ("foo",)
        assert self.kwargs == {"bar": "baz"}
        return 1


containers = CodeCollector()


@containers
def bAMWkT3WSTN1(_app):
    """Task decorator."""

    @contrib.task
    class Container(Injector):

        app = _app
        name = "foo.bar.baz"
        run = Run

    return Container


@containers
def xPa7isagt3Lq(app):
    """Shared task decorator."""

    @contrib.shared_task
    class Container(Injector):

        name = "foo.bar.baz"
        run = Run

    return Container


@containers.parametrize
def test_register_task(celery_app, code):
    """Register Celery task with declarative injector syntax."""

    code(celery_app)
    assert "foo.bar.baz" in celery_app.tasks


@containers.parametrize
def test_execute_task(celery_app, code):
    """Execute task from Celery application."""

    code(celery_app)
    assert celery.signature("foo.bar.baz")("foo", bar="baz") == 1


@containers.parametrize
def test_delay_task(celery_app, code):
    """Delay task from Celery application."""

    ret = code(celery_app)
    assert ret.delay("foo", bar="baz").get() == 1


@containers.parametrize
def test_return_value(celery_app, code):
    """Return `Injector` subclass from register decorator."""

    ret = code(celery_app)
    assert issubclass(ret, Injector)


make_signature = CodeCollector("factory")


@containers.parametrize
@make_signature.parametrize
def test_make_signature(celery_app, code, factory):
    """Insert signature generator into injector."""

    sign = factory(code(celery_app))
    if isinstance(sign, tuple):
        sign, immutable, subtask_type = sign
    else:
        immutable = True
        subtask_type = None
    assert sign._app is celery_app or sign._app is None
    assert sign.task == "foo.bar.baz"
    assert sign.args == (2, 2)
    assert sign.kwargs == {"debug": True}
    assert sign.options == {"countdown": 10}
    assert sign.subtask_type is subtask_type
    assert sign.immutable is immutable


@make_signature
def cgTE4xh2ZSVI(container):
    """Verbose signature."""

    sign = container.signature((2, 2), {"debug": True}, immutable=True, countdown=10)
    return sign


@make_signature
def dUf679YyStBw(container):
    """Verbose signature with options."""

    sign = container.signature(
        (2, 2), {"debug": True}, immutable=True, options={"countdown": 10}
    )
    return sign


@make_signature
def aTMB4bH5LwJh(container):
    """Verbose signature with attributes from container."""

    class NewContainer(container):
        immutable = True
        options = {"countdown": 10}
        subtask_type = "chain"

    sign = NewContainer.signature((2, 2), {"debug": True})
    return sign, True, "chain"


@make_signature
def b2Rm5nGbf27S(container):
    """Verbose signature override attributes from container."""

    class NewContainer(container):
        immutable = False
        options = {"countdown": 1}
        subtask_type = "group"

    sign = NewContainer.signature(
        (2, 2), {"debug": True}, immutable=True, countdown=10, subtask_type="chain"
    )
    return sign, True, "chain"


@make_signature
def kj4SkFAcVOYQ(container):
    """Shortcut signature."""

    class NewContainer(container):
        options = {"countdown": 10}
        subtask_type = "chain"

    sign = NewContainer.s(2, 2, debug=True)
    return sign, False, "chain"


@make_signature
def u4kZae2NSFhE(container):
    """Immutable shortcut signature."""

    class NewContainer(container):
        options = {"countdown": 10}

    sign = NewContainer.si(2, 2, debug=True)
    return sign


def test_docstrings():
    """Access `task` and `shared_task` docstrings."""

    assert contrib.task.__doc__ == "Create Celery task from injector class."
    assert (
        contrib.shared_task.__doc__ == "Create Celery shared task from injector class."
    )

    @contrib.shared_task
    class Container(Injector):
        """Foo bar baz task."""

        name = "foo.bar.baz"
        run = lambda: None  # noqa: E731

    assert Container.__bases__[0].__doc__ == "Foo bar baz task."
    assert (
        Container.signature.__doc__
        == "Create Celery canvas signature with arguments collected from `Injector`\n"
        "    subclass."
    )
    assert Container.s.__doc__ == "Create Celery canvas shortcut expression."
    assert Container.si.__doc__ == "Create immutable Celery canvas shortcut expression."
    assert (
        Container.delay.__doc__
        == "Delay execution of the task defined with `Injector` subclass."
    )


def test_validation(celery_app):
    """Task and shared task decorators must check required `Injector`
    attributes."""

    with pytest.raises(DependencyError) as exc_info:

        @contrib.task
        class Container1(Injector):
            name = "foo.bar.baz"
            run = lambda: None  # noqa: E731

    message = str(exc_info.value)
    assert message == "'Container1' can not resolve attribute 'app'"

    with pytest.raises(DependencyError) as exc_info:

        @contrib.task
        class Container2(Injector):
            app = celery_app
            run = lambda: None  # noqa: E731

    message = str(exc_info.value)
    assert message == "'Container2' can not resolve attribute 'name'"

    with pytest.raises(DependencyError) as exc_info:

        @contrib.task
        class Container3(Injector):
            app = celery_app
            name = "foo.bar.baz"

    message = str(exc_info.value)
    assert message == "'Container3' can not resolve attribute 'run'"

    with pytest.raises(DependencyError) as exc_info:

        @contrib.shared_task
        class Container4(Injector):
            run = lambda: None  # noqa: E731

    message = str(exc_info.value)
    assert message == "'Container4' can not resolve attribute 'name'"

    with pytest.raises(DependencyError) as exc_info:

        @contrib.shared_task
        class Container5(Injector):
            name = "foo.bar.baz"

    message = str(exc_info.value)
    assert message == "'Container5' can not resolve attribute 'run'"


task_arguments = CodeCollector()


@task_arguments.parametrize
def test_task_arguments(celery_app, code):
    """Allow task decorator arguments customization through `Injector` subclass
    attributes."""

    class Foo(object):
        def __call__(self, a, b):
            return a + b

    class Bar(object):
        def __init__(self, foo, task, args, kwargs):
            self.foo = foo
            self.task = task
            self.args = args
            self.kwargs = kwargs

        def do(self):
            one = self.args[0]
            two = self.kwargs["two"]
            assert isinstance(self.task, MyTask)
            return self.foo(one, two)

    class MyTask(celery.Task):
        pass

    code(
        celery_app,
        Injector.let(
            foo=Foo,
            bar=Bar,
            base_class=MyTask,
            bind=True,
            typing=False,
            max_retries=1,
            default_retry_delay=1,
            rate_limit="100/h",
            ignore_result=True,
            trail=False,
            send_events=False,
            store_errors_even_if_ignored=True,
            serializer="yaml",
            time_limit=500,
            soft_time_limit=250,
            track_started=True,
            acks_late=True,
            reject_on_worker_lost=True,
            throws=(ValueError, AttributeError),
        ),
    )

    task_instance = celery_app.tasks["foo.bar.baz"]
    assert task_instance(1, two=2) == 3
    assert isinstance(task_instance, MyTask)
    assert task_instance.typing is False
    assert task_instance.max_retries == 1
    assert task_instance.default_retry_delay == 1
    assert task_instance.rate_limit == "100/h"
    assert task_instance.ignore_result is True
    assert task_instance.trail is False
    assert task_instance.send_events is False
    assert task_instance.store_errors_even_if_ignored is True
    assert task_instance.serializer == "yaml"
    assert task_instance.time_limit == 500
    assert task_instance.soft_time_limit == 250
    assert task_instance.track_started is True
    assert task_instance.acks_late is True
    assert task_instance.reject_on_worker_lost is True
    assert task_instance.throws == (ValueError, AttributeError)


@task_arguments
def z3uG24zlPL7s(_app, container):
    """Task decorator."""

    @contrib.task
    class Container(container):

        app = _app
        name = "foo.bar.baz"
        run = this.bar.do


@task_arguments
def pvRJsuaumvOU(app, container):
    """Shared task decorator."""

    @contrib.shared_task
    class Container(container):

        name = "foo.bar.baz"
        run = this.bar.do

import pytest
from celery import Celery, signature
from dependencies import Injector
from dependencies.contrib.celery import shared_task, task
from helpers import CodeCollector


@pytest.fixture
def celery_app():
    """Simulate global Celery application instance."""

    return Celery()


containers = CodeCollector()


@containers
def bAMWkT3WSTN1(_app):
    """Task decorator."""

    @task
    class Container(Injector):

        app = _app
        name = 'foo.bar.baz'

        def run(*args, **kwargs):
            assert args == ('foo',)
            assert kwargs == {'bar': 'baz'}
            return 1

    return Container


@containers
def xPa7isagt3Lq(app):
    """Shared task decorator."""

    @shared_task
    class Container(Injector):

        name = 'foo.bar.baz'

        def run(*args, **kwargs):
            assert args == ('foo',)
            assert kwargs == {'bar': 'baz'}
            return 1

    return Container


@containers.parametrize
def test_register_task(celery_app, code):
    """Register Celery task with declarative injector syntax."""

    code(celery_app)
    assert 'foo.bar.baz' in celery_app.tasks


@containers.parametrize
def test_execute_task(celery_app, code):
    """Execute task from Celery application."""

    code(celery_app)
    assert signature('foo.bar.baz')('foo', bar='baz') == 1


@containers.parametrize
def test_return_value(celery_app, code):
    """Return `Injector` subclass from register decorator."""

    ret = code(celery_app)
    assert issubclass(ret, Injector)


make_signature = CodeCollector('factory')


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
    assert sign.task == 'foo.bar.baz'
    assert sign.args == (2, 2)
    assert sign.kwargs == {'debug': True}
    assert sign.options == {'countdown': 10}
    assert sign.subtask_type is subtask_type
    assert sign.immutable is immutable


@make_signature
def cgTE4xh2ZSVI(container):
    """Verbose signature."""

    sign = container.signature(
        (2, 2),
        {'debug': True},
        immutable=True,
        countdown=10,
    )
    return sign


@make_signature
def dUf679YyStBw(container):
    """Verbose signature with options."""

    sign = container.signature(
        (2, 2),
        {'debug': True},
        immutable=True,
        options={'countdown': 10},
    )
    return sign


@make_signature
def aTMB4bH5LwJh(container):
    """Verbose signature with attributes from container."""

    class NewContainer(container):
        immutable = True
        options = {'countdown': 10}
        subtask_type = 'chain'

    sign = NewContainer.signature(
        (2, 2),
        {'debug': True},
    )
    return sign, True, 'chain'


@make_signature
def b2Rm5nGbf27S(container):
    """Verbose signature override attributes from container."""

    class NewContainer(container):
        immutable = False
        options = {'countdown': 1}
        subtask_type = 'group'

    sign = NewContainer.signature(
        (2, 2),
        {'debug': True},
        immutable=True,
        countdown=10,
        subtask_type='chain',
    )
    return sign, True, 'chain'


@make_signature
def kj4SkFAcVOYQ(container):
    """Shortcut signature."""

    class NewContainer(container):
        options = {'countdown': 10}
        subtask_type = 'chain'

    sign = NewContainer.s(2, 2, debug=True)
    return sign, False, 'chain'


@make_signature
def u4kZae2NSFhE(container):
    """Immutable shortcut signature."""

    class NewContainer(container):
        options = {'countdown': 10}

    sign = NewContainer.si(2, 2, debug=True)
    return sign


def test_documentation():
    """Access `task` and `shared_task` docstrings."""

    assert task.__doc__ == 'Create Celery task from injector class.'
    assert shared_task.__doc__ == \
        'Create Celery shared task from injector class.'

    @shared_task
    class Container(Injector):
        """Foo bar baz task."""

        name = 'foo.bar.baz'
        run = lambda: None  # noqa: E731

    # FIXME: assert Container.__doc__ == 'Foo bar baz task.'
    assert Container.signature.__doc__ == """
    Create Celery canvas signature with arguments collected from
    `Injector` subclass.
    """
    assert Container.s.__doc__ == 'Create Celery canvas shortcut expression.'
    assert Container.si.__doc__ == \
        'Create immutable Celery canvas shortcut expression.'

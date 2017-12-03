import pytest
from celery import Celery, signature
from dependencies import Injector
from dependencies.contrib.celery import shared_task, task
from helpers import CodeCollector


@pytest.fixture
def celery_app():
    """Simulate global Celery application instance."""

    return Celery()


register_task = CodeCollector()
execute_task = CodeCollector()
return_value = CodeCollector()
make_signature = CodeCollector()


@register_task.parametrize
def test_register_task(celery_app, code):
    """Register Celery task with declarative injector syntax."""

    code(celery_app)
    assert 'foo.bar.baz' in celery_app.tasks


@execute_task.parametrize
def test_execute_task(celery_app, code):
    """Execute task from Celery application."""

    code(celery_app)
    assert signature('foo.bar.baz')('foo', bar='baz') == 1


@return_value.parametrize
def test_return_value(celery_app, code):
    """Return `Injector` subclass from register decorator."""

    ret = code(celery_app)
    assert issubclass(ret, Injector)


@make_signature.parametrize
def test_make_signature(celery_app, code):
    """Insert signature generator into injector."""

    ret = code(celery_app)
    sign = ret.signature((2, 2), {'debug': True}, immutable=True, countdown=10)
    assert sign._app is celery_app or sign._app is None
    assert sign.task == 'foo.bar.baz'
    assert sign.args == (2, 2)
    assert sign.kwargs == {'debug': True}
    assert sign.options == {'countdown': 10}
    assert sign.subtask_type is None  # TODO: ?
    assert sign.immutable is True


@register_task
@execute_task
@return_value
@make_signature
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


@register_task
@execute_task
@return_value
@make_signature
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


def test_documentation():
    """Access `task` and `shared_task` docstrings."""

    assert task.__doc__ == 'Create Celery task from injector class.'
    assert shared_task.__doc__ == \
        'Create Celery shared task from injector class.'

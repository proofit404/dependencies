"""
dependencies.contrib.celery
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements injectable Celery task definition.

:copyright: (c) 2016-2017 by Artem Malyshev.
:license: LGPL-3, see LICENSE for more details.
"""

from __future__ import absolute_import

import celery
from dependencies import Injector

__all__ = ['task', 'shared_task']


class Signature(object):
    """
    Create Celery canvas signature with arguments collected from
    `Injector` subclass.
    """

    def __init__(self, name, app=None):

        self.name = name
        self.app = app

    def __call__(self, args=None, kwargs=None, immutable=False, **ex):

        return celery.canvas.Signature(
            task=self.name,
            app=self.app,
            args=args,
            kwargs=kwargs,
            immutable=immutable,
            **ex)


class TaskMixin(Injector):
    """
    Inject `signature` attribute and `s` shortcut into `Injector`
    subclass.
    """
    signature = Signature


def task(injector):
    """Create Celery task from injector class."""

    @injector.app.task(name=injector.name)
    def __task(*args, **kwargs):
        return injector.run(*args, **kwargs)

    return TaskMixin & injector


def shared_task(injector):
    """Create Celery shared task from injector class."""

    @celery.shared_task(name=injector.name)
    def __task(*args, **kwargs):
        return injector.run(*args, **kwargs)

    return TaskMixin & injector


# TODO:
#
# Assert injector has necessary attributes with custom error message.
#
# Support all arguments of the `s`, `si`, `signature` and `task`.

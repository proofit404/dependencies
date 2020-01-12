from __future__ import absolute_import

import celery.canvas

from _dependencies.injector import Injector


undefined = object()


def task(injector):
    """Create Celery task from injector class."""

    return decorate_with(injector.app.task, injector)


def shared_task(injector):
    """Create Celery shared task from injector class."""

    return decorate_with(celery.shared_task, injector)


def decorate_with(func, injector):

    if "run" not in injector:
        injector.run

    options = {"name": injector.name}

    if "base_class" in injector:
        options["base"] = injector.base_class

    for argument in [
        "bind",
        "typing",
        "max_retries",
        "default_retry_delay",
        "rate_limit",
        "ignore_result",
        "trail",
        "send_events",
        "store_errors_even_if_ignored",
        "serializer",
        "time_limit",
        "soft_time_limit",
        "track_started",
        "acks_late",
        "reject_on_worker_lost",
        "throws",
    ]:
        if argument in injector:
            options[argument] = getattr(injector, argument)

    if "bind" in injector and injector.bind:

        def __task(self, *args, **kwargs):
            return injector.let(task=self, args=args, kwargs=kwargs).run()

    else:

        def __task(*args, **kwargs):  # type: ignore
            return injector.let(args=args, kwargs=kwargs).run()

    func(**options)(__task)

    return injector & TaskMixin


class Signature(object):
    """Create Celery canvas signature with arguments collected from `Injector`
    subclass."""

    def __init__(
        self,
        name,
        app=None,
        immutable=undefined,
        options=undefined,
        subtask_type=undefined,
    ):

        self.name = name
        self.app = app
        self.immutable = immutable
        self.options = options
        self.subtask_type = subtask_type

    def __call__(self, args=None, kwargs=None, **ex):

        if "options" not in ex and self.options is not undefined:
            ex["options"] = self.options
        if "immutable" not in ex and self.immutable is not undefined:
            ex["immutable"] = self.immutable
        if "subtask_type" not in ex and self.subtask_type is not undefined:
            ex["subtask_type"] = self.subtask_type
        return celery.canvas.Signature(
            task=self.name, app=self.app, args=args, kwargs=kwargs, **ex
        )


class Shortcut(Signature):
    """Create Celery canvas shortcut expression."""

    immutable_default = False

    def __call__(self, *args, **kwargs):

        return celery.canvas.Signature(
            task=self.name,
            app=self.app,
            args=args,
            kwargs=kwargs,
            immutable=(
                self.immutable_default
                if self.immutable is undefined
                else self.immutable
            ),
            options={} if self.options is undefined else self.options,
            subtask_type=(
                None if self.subtask_type is undefined else self.subtask_type
            ),
        )


class ImmutableShortcut(Shortcut):
    """Create immutable Celery canvas shortcut expression."""

    immutable_default = True


class Delay(Signature):
    """Delay execution of the task defined with `Injector` subclass."""

    def __call__(self, *args, **kwargs):

        signature = super(Delay, self).__call__()
        return signature.delay(*args, **kwargs)


class TaskMixin(Injector):  # type: ignore

    signature = Signature
    s = Shortcut
    si = ImmutableShortcut
    delay = Delay

from typing import Callable, Dict, Optional, Tuple, Union

from celery.app.base import Celery
from celery.canvas import Signature as _Signature
from celery.result import EagerResult

from dependencies._injector import Injector


def task(injector: Injector) -> Injector: ...


def shared_task(injector: Injector) -> Injector: ...


def decorate_with(func: Callable, injector: Injector) -> Injector: ...


class Signature:

    def __init__(
        self,
        name: str,
        app: Optional[Celery] = ...,
        immutable: Union[bool, object] = ...,
        options: Union[object, Dict[str, int]] = ...,
        subtask_type: Union[str, object] = ...,
    ) -> None: ...

    def __call__(
        self,
        args: Optional[Tuple[int, int]] = ...,
        kwargs: Optional[Dict[str, bool]] = ...,
        **ex
    ) -> _Signature: ...


class Shortcut:

    def __call__(self, *args, **kwargs) -> Signature: ...


class ImmutableShortcut:

    def __call__(self, *args, **kwargs) -> Signature: ...


class Delay:

    def __call__(self, *args, **kwargs) -> EagerResult: ...


class TaskMixin:
    ...

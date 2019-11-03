from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

from celery.app.base import Celery
from celery.canvas import Signature as _Signature
from celery.result import EagerResult

from _dependencies.injector import Injector

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
        **ex: Any
    ) -> _Signature: ...

class Shortcut:
    def __call__(self, *args: Any, **kwargs: Any) -> Signature: ...

class ImmutableShortcut:
    def __call__(self, *args: Any, **kwargs: Any) -> Signature: ...

class Delay:
    def __call__(self, *args: Any, **kwargs: Any) -> EagerResult: ...

class TaskMixin: ...

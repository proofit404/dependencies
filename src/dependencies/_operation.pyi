from functools import partial
from typing import Any, Callable, Dict, List, Tuple


class Operation:

    def __init__(self, function: Callable) -> None: ...


def make_operation_spec(
    dependency: Operation
) -> Tuple[str, OperationSpec, List[str], int]: ...


class OperationSpec:

    def __init__(self, func: Callable) -> None: ...

    def __call__(self, **kwargs: Dict[str, Any]) -> partial: ...

    @property
    def __name__(self) -> str: ...

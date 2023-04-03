from __future__ import annotations

from collections.abc import Callable
from inspect import signature
from typing import Generic
from typing import overload
from typing import TypeVar


A = TypeVar("A")
B = TypeVar("B")


@overload
def wire(dependency: type[A]) -> Init[A, A]:
    raise RuntimeError


@overload
def wire(dependency: type[A], callback: Callable[[A], B]) -> Init[A, B]:
    raise RuntimeError


def wire(dependency: type[A], callback: Callable[[A], B] | None = None) -> Init[A, B]:
    return Init(dependency, callback or identity)  # type: ignore[arg-type]


C = TypeVar("C")
D = TypeVar("D")


class Init(Generic[C, D]):
    def __init__(self, dependency: type[C], callback: Callable[[C], D]) -> None:
        self.dependency = dependency
        self.callback = callback
        self.args = args(dependency.__init__)[1:]

    def __get__(self, instance: object, owner: type[object]) -> D:
        return self.callback(
            self.dependency(
                **{arg: getattr(owner, arg) for arg in self.args}  # type: ignore[misc]
            )
        )


def identity(x: object) -> object:
    return x


def args(func: Callable[[object], None]) -> list[str]:
    return list(signature(func).parameters)

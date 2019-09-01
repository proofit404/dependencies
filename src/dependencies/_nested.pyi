from typing import Any, Dict, List, Tuple, Type, Union

from dependencies import Injector
from dependencies._attributes import Attributes
from dependencies._package import ImportSpec
from dependencies._raw import RawSpec
from dependencies._this import ThisSpec


def make_nested_injector_spec(
    dependency: Type[Injector]
) -> Tuple[str, NestedInjectorSpec, List[str], int]: ...


class NestedInjectorSpec:

    def __init__(self, injector: Injector) -> None: ...

    def __call__(self, __self__: Injector) -> Type[Injector]: ...

    @property
    def __dependencies__(
        self
    ) -> Dict[
        str,
        Union[
            Tuple[str, ThisSpec, List[str], int],
            Tuple[str, Attributes, List[str], int],
            Tuple[str, RawSpec, List[Any], int],
            Tuple[str, NestedInjectorSpec, List[str], int],
            Tuple[str, ImportSpec, List[Any], int],
        ],
    ]: ...

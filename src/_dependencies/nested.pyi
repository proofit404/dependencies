from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type
from typing import Union

from _dependencies.attributes import Attributes
from _dependencies.injector import Injector
from _dependencies.package import ImportSpec
from _dependencies.raw import RawSpec
from _dependencies.this import ThisSpec

def make_nested_injector_spec(
    dependency: Type[Injector],
) -> Tuple[str, NestedInjectorSpec, List[str], int]: ...

class NestedInjectorSpec:
    def __init__(self, injector: Injector) -> None: ...
    def __call__(self, __self__: Injector) -> Type[Injector]: ...
    @property
    def __dependencies__(
        self,
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

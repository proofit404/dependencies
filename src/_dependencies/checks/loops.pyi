from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Tuple
from typing import Union

from _dependencies.attributes import Attributes
from _dependencies.nested import NestedInjectorSpec
from _dependencies.this import ThisSpec

def check_loops(class_name: str, dependencies: Dict[str, Any]) -> None: ...
def check_loops_for(
    class_name: str,
    attribute_name: str,
    dependencies: Dict[str, Any],
    origin: Tuple[str, ThisSpec, List[str], int],
    expression: Iterator[Any],
) -> None: ...
def filter_expression(spec: ThisSpec) -> Iterator[str]: ...
def nested_dependencies(
    parent: Dict[str, Any],
    spec: Union[
        Tuple[str, Attributes, List[str], int],
        Tuple[str, NestedInjectorSpec, List[str], int],
    ],
) -> Dict[str, Any]: ...

from typing import Any, Dict, Iterator, List, Tuple, Union

from dependencies._attributes import Attributes
from dependencies._nested import NestedInjectorSpec
from dependencies._this import ThisSpec


def check_loops(class_name: str, dependencies: Dict[str, Any]) -> None: ...


def check_loops_for(
    class_name: str,
    attribute_name: str,
    dependencies: Dict[str, Any],
    origin: Tuple[str, ThisSpec, List[str], int],
    expression: Iterator[Any],
) -> None: ...


def filter_expression(spec) -> Iterator[str]: ...


def nested_dependencies(
    parent: Dict[str, Any],
    spec: Union[
        Tuple[str, Attributes, List[str], int],
        Tuple[str, NestedInjectorSpec, List[str], int],
    ],
) -> Dict[str, Any]: ...

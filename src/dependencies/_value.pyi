from typing import Callable, List, Tuple


class Value:

    def __init__(self, function: Callable) -> None: ...


def make_value_spec(dependency: Value) -> Tuple[str, Callable, List[str], int]: ...

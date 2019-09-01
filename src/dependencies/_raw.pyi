from typing import Any, List, Tuple


def make_raw_spec(dependency: Any) -> Tuple[str, RawSpec, List[Any], int]: ...


class RawSpec:

    def __init__(self, dependency: Any) -> None: ...

    def __call__(self) -> Any: ...

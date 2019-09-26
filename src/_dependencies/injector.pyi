from typing import Any, Dict, Tuple


class Injector:

    def __init__(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None: ...

    @classmethod
    def let(cls, **kwargs: Dict[str, Any]) -> Injector: ...

from typing import Any
from typing import Dict
from typing import Tuple

class Injector:
    def __init__(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None: ...
    @classmethod
    def let(cls, **kwargs: Dict[str, Any]) -> Injector: ...

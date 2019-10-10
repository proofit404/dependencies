from typing import Any
from typing import Dict

def check_circles(dependencies: Dict[str, Any]) -> None: ...
def check_circles_for(
    dependencies: Dict[str, Any], attrname: str, origin: str
) -> None: ...

from typing import List
from typing import Optional

def check_cls_arguments(
    argnames: List[str], defaults: List[int], owner_message: str
) -> None: ...
def check_varargs(
    name: str, varargs: Optional[bool], kwargs: Optional[bool]
) -> None: ...

from typing import Callable
from typing import List
from typing import Tuple

def make_func_spec(
    func: Callable, funcname: str, owner_message: str
) -> Tuple[List[str], int]: ...

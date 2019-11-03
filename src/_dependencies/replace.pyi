from _dependencies.attributes import Replace
from _dependencies.injector import Injector

def deep_replace_dependency(
    injector: Injector, current_attr: str, replace: Replace
) -> None: ...

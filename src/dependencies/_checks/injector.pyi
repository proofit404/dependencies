from typing import List, Type

from dependencies._injector import Injector


def check_inheritance(bases: List[Type], injector: Injector) -> None: ...


def check_dunder_name(name: str) -> None: ...


def check_attrs_redefinition(name: str) -> None: ...

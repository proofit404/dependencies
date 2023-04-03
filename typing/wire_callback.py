from dataclasses import dataclass
from typing import assert_type

from dependencies import wire


@dataclass
class User:
    name: str
    age: int


def getname(user: User) -> str:
    return user.name


class Container:
    username = wire(User, getname)
    name = "Kate"
    age = 18


assert_type(Container.username, str)

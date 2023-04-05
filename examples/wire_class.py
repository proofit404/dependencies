from dataclasses import dataclass
from typing import assert_type

from dependencies import wire


@dataclass
class User:
    name: str

    def greet(self) -> str:
        return f"Hello, {self.name}"


class Container:
    user = wire(User)
    name = "John"


assert_type(Container.user, User)


print(Container.user.greet())

from dataclasses import dataclass

from dependencies import wire


def test_instantiate() -> None:
    @dataclass
    class User:
        name: str
        age: int

    class Container:
        user = wire(User)
        name = "John"
        age = 27

    assert Container.user.name == "John"
    assert Container.user.age == 27


def test_callback() -> None:
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

    assert Container.username == "Kate"

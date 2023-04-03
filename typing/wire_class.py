from typing import assert_type

from dependencies import wire


class User:
    ...


class Container:
    user = wire(User)


assert_type(Container.user, User)

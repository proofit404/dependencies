from random import choice
from random import randint
from string import ascii_letters


def _rnd():
    return "".join(choice(ascii_letters) for i in range(randint(8, 24)))

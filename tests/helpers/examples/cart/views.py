from dependencies import Injector
from dependencies.contrib.django import view


@view
class ShowCartWithDiscount(Injector):
    pass

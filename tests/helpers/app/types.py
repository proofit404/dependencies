# -*- coding: utf-8 -*-
from app.purchase import PaypalService
from app.purchase import SMSService


class TypedInjector:
    def register(self, arg):
        pass

    def build(self, arg):
        return arg(PaypalService(), SMSService())

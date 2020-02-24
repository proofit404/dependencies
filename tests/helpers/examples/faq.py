# -*- coding: utf-8 -*-
class AbstractNotificationService:
    pass


class AbstractPaymentService:
    pass


class TypedInjector:
    def register(self, arg):
        pass

    def build(self, arg):
        return arg(PaypalService(), SMSService())


class SMSService(AbstractNotificationService):
    pass


class PaypalService(AbstractPaymentService):
    pass

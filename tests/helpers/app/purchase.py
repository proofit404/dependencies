# -*- coding: utf-8 -*-
class AbstractNotificationService:
    pass


class AbstractPaymentService:
    pass


class SMSService(AbstractNotificationService):
    pass


class PaypalService(AbstractPaymentService):
    pass

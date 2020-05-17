# -*- coding: utf-8 -*-
class AbstractNotificationService:
    """Service interface declaration."""

    pass


class AbstractPaymentService:
    """Service interface declaration."""

    pass


class SMSService(AbstractNotificationService):
    """Service implementation."""

    pass


class PaypalService(AbstractPaymentService):
    """Service implementation."""

    pass

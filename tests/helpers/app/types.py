# -*- coding: utf-8 -*-
from app.purchase import PaypalService
from app.purchase import SMSService


class TypedInjector:
    """Alternative Injector API approach."""

    def register(self, arg):
        """Register interface implementation."""
        pass

    def build(self, arg):
        """Instantiate."""
        return arg(PaypalService(), SMSService())

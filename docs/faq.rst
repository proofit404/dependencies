============================
 Frequently asked questions
============================

Why do not use type annotations?
================================

It is possible to look for types of ``__init__`` arguments instead of
names.  Obviously, code written in this style will look something like
this:

.. code:: python

    class ApplicationService:

        def __init__(
            self,
            payment_gateway: AbstractPaymentService,
            notification_gateway: AbstractNotificationService
        ):
            self.payment_gateway = payment_gateway
            self.notification_gateway = notification_gateway

    container = Injector()
    container.register(ApplicationService)
    container.register(SMSService)
    container.register(PaypalService)

In our opinion, this makes code less declarative.

* It hard to tell what dependencies will be resolved based on
  container definition.  You need to look at many different things at
  the time: a signature of the ``__init__`` method, container
  definition, base type of each class registered in the container.
* Container definition can be split into different files which make it
  harder to read.
* It hard to define multiple dependencies of the same type in one
  container.  For example, your service needs two databases to work
  with.  You need to define two different classes for types signatures
  and then define two different database classes.

This lead to unnecessary boilerplate.

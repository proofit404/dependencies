# Why do not use type annotations?

It is possible to look for types of `__init__` arguments instead of names.
Obviously, code written in this style will look something like this:

```pycon

>>> from app.types import TypedInjector
>>> from app.purchase import (
...     AbstractPaymentService,
...     PaypalService,
...     AbstractNotificationService,
...     SMSService,
... )

>>> class PurchaseService:
...     def __init__(
...         self,
...         payments: AbstractPaymentService,
...         notifications: AbstractNotificationService,
...     ):
...         self.payments = payments
...         self.notifications = notifications

>>> container = TypedInjector()
>>> container.register(SMSService)
>>> container.register(PaypalService)
>>> container.build(PurchaseService)  # doctest: +ELLIPSIS
<__main__.PurchaseService object at 0x...>

```

In our opinion, this makes code less declarative.

1. **It's hard to tell how dependencies will be resolved.** At the same time,
   looking on container definition and a signature of the `__init__` method can
   you easily say what arguments will be passed to the constructor? You can't.
   You will need to inspect all superclasses of each dependency registered in
   the container. With our `Injector` approach, you don't have this problem. You
   will find arguments right in the `Injector` subclass in one place.
2. **It's a global mutable variable.** Container definition can be split into
   different files. This will make it harder to read. It's similar to the
   service locator. Many architect people consider it an anti-pattern.
3. **It hard to define multiple dependencies of the same type.** For example,
   your service needs two databases to work with. You need to define two
   different classes for types signatures and then define two different database
   classes. The same is necessary for these classes arguments. Both of them
   needs a port to run. How would you name it? `PrimaryDatabasePort` and
   `SecondaryDatabasePort` instead of `int`? This leads to unnecessary
   boilerplate.

<p align="center">&mdash; ⭐ &mdash;</p>

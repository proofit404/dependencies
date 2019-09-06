# FAQ

## Why do not use type annotations?

It is possible to look for types of `__init__` arguments instead of
names. Obviously, code written in this style will look something like
this:

```pycon

>>> from examples.faq import AbstractNotificationService, \
...                          AbstractPaymentService, \
...                          TypedInjector, SMSService, PaypalService

>>> class ApplicationService:
...
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
>>> container.build(ApplicationService)  # doctest: +ELLIPSIS
<__main__.ApplicationService object at 0x...>

```

In our opinion, this makes code less declarative.

1. **It hard to tell how dependencies will be resolved.** At the same
   time looking on container definition and a signature of the
   `__init__` method can you easily say what arguments will be passed
   to the constructor?  You can't. You need to inspect a base class of
   each dependency registered in the container.  With our `Injector`
   approach, you don't have this problem. You will find arguments
   right in the `Injector` subclass in one place.
2. **It's a global mutable variable.** Container definition can be
   split into different files. This will make it harder to read.  It's
   very similar to the service locator. Many architect people consider
   it an anti-pattern.
3. **It hard to define multiple dependencies of the same type.** For
   example, your service needs two databases to work with. You need to
   define two different classes for types signatures and then define
   two different database classes.  The same is necessary for these
   classes arguments. Both of them needs a port to run. How would you
   name it? `PrimaryDatabasePort` and `SecondaryDatabasePort` instead
   of `int`?  This lead to unnecessary boilerplate.

## Mixins considered harmful

`dependencies` are compared with mixins often. In a sense that both
solutions were made to maximize code reuse. We already discussed this in
the [why](why.md#mixins) chapter. But let's return to it again:

!!! note
    Inheritance always breaks encapsulation.

Mixin class depends on attributes set in other classes.

Consider this code snippet:

```pycon

>>> class RetrieveModelMixin(object):
...     """
...     Retrieve a model instance.
...     """
...     def retrieve(self, request, *args, **kwargs):
...         instance = self.get_object()
...         serializer = self.get_serializer(instance)
...         return Response(serializer.data)

```

Where `get_object` and `get_serializer` were defined? We have no idea.
We are thinking that code below is way better for understanding its
structure.

```pycon

>>> class RetrieveModel(object):
...     """
...     Retrieve a model instance.
...     """
...     def __init__(self, get_object, get_serializer):
...         self.get_object = get_object
...         self.get_serializer = get_serializer
...
...     def retrieve(self, request, *args, **kwargs):
...         instance = self.get_object()
...         serializer = self.get_serializer(instance)
...         return Response(serializer.data)

```

## What inject and what not inject

It can be hard to draw the border between what should be injectable and
what not. Let's consider this typical example.

```pycon

>>> import requests
>>> import dependencies

>>> class UserGetter:
...
...     def __init__(self, http):
...         self.http = http
...
...     def __call__(self, user_id):
...         return self.http.get("http://api.com/users/%d/" % (user_id,)).json()

>>> class Users(dependencies.Injector):
...
...     get = UserGetter
...     http = requests

>>> Users.get(1)
{'id': 1, 'name': 'John', 'surname': 'Doe'}

```

1. Should I write code like this?
2. Will I ever decide to use something other than excellent
   [requests](http://docs.python-requests.org/) library?

In our opinion that are not right questions to ask.

By injecting a certain library you add a **hard** dependency on its
interfaces to the whole systems. Migration to other libraries in the
future can be painful.

Also, this adds another **hard** dependency to the whole system. Your
code depends on the structure of third-party API response. This makes
the situation even worth. Migration to other third-party services will
be painful as well.

We believe that HTTP protocol itself is implementation detail!

We prefer to use dependency injection only on boundaries we control:

```pycon

>>> import dataclasses
>>> import dependencies
>>> import requests

>>> class HomePage:
...
...     def __init__(self, get_user):
...         self.get_user = get_user
...
...     def show(self, user_id):
...         user = self.get_user(user_id=user_id)

>>> @dataclasses.dataclass
... class UserStruct:
...
...     id: int
...     name: str
...     surname: str

>>> def get_user(user_id):
...
...     response = requests.get("http://api.com/users/%d/" % (user_id,))
...     return UserStruct(**response.json())

>>> class Site(dependencies.Injector):
...
...     home_page = HomePage
...     get_user = get_user

>>> Site.home_page.show(1)

```

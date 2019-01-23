=====
 FAQ
=====

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

Mixins considered harmful
=========================

``dependencies`` are compared with mixins often.  In a sense that both
solutions were made to maximize code reuse.  We already discussed this
in the `why`_ chapter.  But let's return to it again::

    Inheritance always breaks encapsulation.

Consider this code snippet:

.. code:: python

    class RetrieveModelMixin(object):
        """
        Retrieve a model instance.
        """
        def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

Where ``get_object`` and ``get_serializer`` were defined?  We have no
idea.  We are thinking that code below is way better for understanding
its structure.

.. code:: python

    class RetrieveModel(object):
        """
        Retrieve a model instance.
        """
        def __init__(self, get_object, get_serializer):
            self.get_object = get_object
            self.get_serializer = get_serializer

        def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

What inject and what not inject
===============================

It can be hard to draw the border between what should be injectable
and what not.  Let's consider this typical example.

.. code:: python

    import requests
    import dependencies

    class UserGetter:

        def __init__(self, http):
            self.http = http

        def __call__(self, user_id):
            return self.http.get("http://api.com/users/%d" % (user_id,))

    class Users(dependencies.Injector):

        get = UserGetter
        http = requests

    Users.get(1)
    # {'id': 1, 'name': 'John', 'surname': 'Doe'}

* Should I write code like this?
* Will I ever decide to use something other than excellent `requests`_
  library?

In our opinion that are not right questions to ask.

By injecting a certain library you add a **hard** dependency on its
interfaces to the whole systems.  Migration to other libraries in the
future can be painful.

Also, this adds another **hard** dependency to the whole system.  Your
code depends on the structure of third-party API response.  This makes
the situation even worth.  Migration to other third-party services
will be painful as well.

We believe that HTTP protocol itself is implementation detail!

We prefer to use dependency injection only on boundaries we control:

.. code:: python

    import dataclasses
    import dependencies
    import requests

    class HomePage:

        def __init__(self, get_user):
            self.get_user = get_user

        def show(sefl):
            user = self.get_user(1)

    @dataclasses.dataclass
    class UserStruct:

        id: int
        name: str
        surname: str

    def get_user(user_id):

        response = requests.get(user_id)
        return UserStruct(**response)

    class Site(dependencies.Injector):

        home_page = HomePage
        get_user = get_user

    Site.home_page.show()

.. _why: why.html#mixins
.. _requests: http://docs.python-requests.org/

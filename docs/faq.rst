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

.. _why: why.html#mixins

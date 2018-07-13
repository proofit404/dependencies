================
 Django contrib
================

Integration with Django framework provides way to define class-based
and form processing views.  This way you can pass injector subclass
directly to the url config.

Class-based views
=================

Let's start with Django url patterns.

.. code:: python

    from django.urls import path

    from .views import ShowCartWithDiscount

    urlpatterns = [
        path('cart/<int:pk>/items/', ShowCartWithDiscount.as_view()),
    ]

Looks familiar, right?  Now let's take a look at the views module.

.. code:: python

    from dependencies import Injector, operation, this
    from dependencies.contrib.django import view

    from .commands import ShowCart, DiscountCalc

    @view
    class ShowCartWithDiscount(Injector):

        @operation
        def get(show_cart, pk):
            return show_cart.show(cart_id=pk)

        show_cart = ShowCart
        price_calc = DiscountCalc

You can see that instead of classic Django class-based view we found
injector subclass with ``view`` decorator applied to it.  ``view``
decorator keep your injector as it is except one thing.  It add
``as_view`` function to its scope.  This function return actual
class-based view instance ready to dispatch request.

Request will be dispatched based on it's HTTP method.  To process any
HTTP verb injector should contains callable attribute named the same
way.  Following verbs are supported ``get``, ``post``, ``put``,
``patch``, ``delete``, ``head``, ``options``, ``trace``.  This
callable should take no parameters.  Everything it need to work should
be it dependency.  ``operation`` decorator is excellent candidate for
this.

Now let's take a look into actual business logic representation.

.. code:: python

    class ShowCart(object):
        def __init__(self, price_calc):
            pass

        def show(self, cart_id):
            pass

    class DiscountCalc(object):
        pass

Available scope
---------------

Dependency injecting happens before request processing.  ``view``
decorator takes a responsibility to populate injection scope with
information related to the current request.

* ``view`` actual class-based view instance processing request.

* ``request`` current request.  First view function argument.

* ``args`` view positional arguments taken from url.  This is a result
  of path converters application or regular expression non-named
  groups taken from an actual URL.

* ``kwargs`` view keyword arguments.

* ``user`` current user taken from request.  A short cat for
  frequently used request attribute.

* ``pk`` primary key view argument.  A short cat for frequently used
  keyword argument.

Form processing views
=====================

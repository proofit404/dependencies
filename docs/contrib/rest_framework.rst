========================
 REST Framework contrib
========================

Django REST framework integration provides an ability to define
regular and generic API views and model view sets.  This way you can
add injector subclasses to the django url config and to DRF routers.

API views
=========

As with Django itself, we will start from the url config.

.. code:: python

    # app/urls.py

    from django.urls import path

    from .views import CartAPIView

    urlpatterns = [
        path('api/carts/<int:pk>/', CartAPIView.as_view())
    ]

View definition will be similar to the Django one.  The difference is
in the actual view base class.  It will be ``APIView`` subclass.  You
are able to setup it's attributes like authentication, render and
parser classes.

.. code:: python

    # app/views.py

    from dependencies import Injector, this
    from dependencies.contrib.rest_framework import api_view
    from rest_framework.parsers import JSONParser
    from rest_framework.renderers import DocumentationRenderer

    from .commands import ShowCartDetails, AddCartItem

    @api_view
    class CartAPIView(Injector):

        get = ShowCartDetails
        post = AddCartItem

        renderer_classes = (DocumentationRenderer,)
        parser_classes = (JSONParser,)

HTTP verb handlers can be specified in the ``get``, ``post``, ``put``,
``patch``, ``delete``, ``head``, ``options``, ``trace`` attributes.
Them should be callables which takes no arguments.

.. code:: python

    # app/commands.py

    class ShowCartDetails(object):
        def __init__(self, pk):
            pass

        def __call__(self):
            pass

Customizable arguments
----------------------

In addition to the HTTP verb handlers, you can set up following
arguments to customize ``APIView`` under the hood.

* ``authentication_classes``

* ``renderer_classes``

* ``parser_classes``

* ``throttle_classes``

* ``permission_classes``

* ``content_negotiation_class``

* ``versioning_class``

* ``metadata_class``

The meaning of each attribute can be found in the REST framework
documentation.

Available scope
---------------

Injector scope of the API view extended the same way as django
class-based view scope.  ``view``, ``request``, ``args``, ``kwargs``,
``user`` and ``pk`` arguments are added and can be used as arguments
in the constructor of the HTTP verb handler.

Generic API View
================

You are free to use ``GenericAPIView`` as a base class to your views.
This is useful if you want to have access to the to the view methods.
For example, delegate queryset and serializer processing to the view.

.. code:: python

    # app/views.py

    from dependencies import Injector
    from dependencies.contrib.rest_framework import generic_api_view

    from .commands import ListCartItems

    @generic_api_view
    class CartItemListView(Injector):

        get = ListCartItems

        queryset = Item.objects.all()
        serializer_class = ItemSerializer
        filter_backends = (DjangoFilterBackend,)
        filter_class = CartFilter

Business logic can use view instance.

.. code:: python

    # app/commands.py

    class ListCartItems(object):

        def __init__(self, view, request):
            pass

        def __call__(self):

            items = self.view.get_queryset()
            items = self.view.filter_queryset(items)
            page = self.view.paginate_queryset(items)
            # Business logic work with `page`.
            # ...
            serializer = self.view.get_serializer(page, many=True)
            return self.view.get_paginated_response(serializer.data)

Customizable arguments
----------------------

As with all ``view`` related decorators you can specified handlers of
HTTP verbs.  ``get``, ``post``, ``put``, ``patch``, ``delete``,
``head``, ``options``, ``trace`` attributes works as usual.

In addition you can set following attributes and they will be passed
to the ``GenericAPIView`` subclass under the hood.  Everything works
according to the rest framework documentation.

* ``queryset``
* ``serializer_class``
* ``lookup_field``
* ``lookup_url_kwarg``
* ``filter_backends``
* ``filter_class``
* ``pagination_class``

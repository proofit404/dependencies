# REST Framework contrib

Django REST framework integration provides an ability to define regular
and generic API views and model view sets. This way you can add injector
subclasses to the django url config and to DRF routers.

## API views

As with Django itself, we will start from the url config.

```python
# app/urls.py

from django.urls import path

from .views import CartAPIView

urlpatterns = [
    path('api/carts/<int:pk>/', CartAPIView.as_view())
]
```

View definition will be similar to the Django one. The difference is in
the actual view base class. It will be `APIView` subclass. You are able
to setup it's attributes like authentication, render and parser classes.

```python
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
```

HTTP verb handlers can be specified in the `get`, `post`, `put`,
`patch`, `delete`, `head`, `options`, `trace` attributes. Them should be
callables which takes no arguments.

```python
# app/commands.py

class ShowCartDetails(object):
    def __init__(self, pk):
        pass

    def __call__(self):
        pass
```

### Customizable arguments

In addition to the HTTP verb handlers, you can set up following
arguments to customize `APIView` under the hood.

  - `authentication_classes`
  - `renderer_classes`
  - `parser_classes`
  - `throttle_classes`
  - `permission_classes`
  - `content_negotiation_class`
  - `versioning_class`
  - `metadata_class`

The meaning of each attribute can be found in the REST framework
documentation.

### Available scope

Injector scope of the API view extended the same way as django
class-based view scope. `view`, `request`, `args`, `kwargs`, `user` and
`pk` arguments are added and can be used as arguments in the constructor
of the HTTP verb handler.

## Generic API View

You are free to use `GenericAPIView` as a base class to your views. This
is useful if you want to have access to the to the view methods. For
example, delegate queryset and serializer processing to the view.

```python
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
```

Business logic can use view instance.

```python
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
```

### Customizable arguments

As with all `view` related decorators you can specified handlers of HTTP
verbs. `get`, `post`, `put`, `patch`, `delete`, `head`, `options`,
`trace` attributes works as usual.

In addition to `api_view` attributes you can set following attributes
and they will be passed to the `GenericAPIView` subclass under the hood.
Everything works according to the rest framework documentation.

  - `queryset`
  - `serializer_class`
  - `lookup_field`
  - `lookup_url_kwarg`
  - `filter_backends`
  - `filter_class`
  - `pagination_class`

## Model View Set

Also, it is possible to define complete `ModelViewSet` from the injector
and add it to the rest framework router.

```python
# app/urls.py

router = SimpleRouter()
router.register(r"users", UserViewSet.as_viewset())

urlpatterns = [
    url(r"^", include(router.urls)),
]
```

Use `as_viewset` method to register the `UserViewSet` class in the
router. Its implementation should looks something like this.

```python
# app/views.py

from dependencies import Injector
from dependencies.contrib.rest_framework import model_view_set

from .commands import CreateUser, UpdateUser, DestroyUser

@model_view_set
class UserViewSet(Injector):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    create = CreateUser
    update = UpdateUser
    destroy = DestroyUser
```

`model_view_set` decorator gives you an ability to redefine
`perform_create`, `perform_update` and `perform_destroy` methods of the
`ModelViewSet`.

```python
# app/commands.py

class CreateUser(object):

    def __init__(self, user, validated_data):
        pass

    def __call__(self):
        # Business logic here.
        # You should return created model instance.
        return User.objects.create(**self.validated_data)

class DestroyUser(object):

    def __init__(self, user, instance):
        pass

    def __call__(self):
        # Cleanup business logic here.
        pass
```

As you can see from the example above create and update actions get
access to the `serializer` instance from the view. Destroy action get
access to the model `instance` to be destroyed.

### Customizable arguments

Are the same to generic class based view. Except you can not specify
HTTP verbs handlers. You should set `create`, `update` and `destroy`
handlers instead. Everything should resolve to a callable which takes no
arguments.

### Available scope

In addition to the regular view extended scope (`view`, `request`,
`args`, `kwargs`, `user` and `pk`) you have access to this dependencies
in your action constructor.

  - `validated_data` serializer instance attribute in create and update
    actions,
  - `instance` model instance in update and destroy actions,
  - `action` name of the action on the Resource.

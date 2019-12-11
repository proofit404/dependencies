# Django contrib

Integration with Django framework provides a way to define class-based
and form processing views. This way you can pass injector subclass
directly to the url config.

## Class-based views

Let's start with Django url patterns.

```pycon

>>> # cart/urls.py

>>> from django.urls import path
>>> from examples.cart.views import ShowCartWithDiscount

>>> urlpatterns = [
...     path('cart/<int:pk>/items/', ShowCartWithDiscount.as_view()),
... ]

```

Looks familiar, right? Now let's take a look at the views module.

```pycon

>>> # cart/views.py

>>> from dependencies import Injector, operation, this
>>> from dependencies.contrib.django import view

>>> from examples.cart.commands import ShowCart, DiscountCalc

>>> @view
... class ShowCartWithDiscount(Injector):
...
...     show_cart = ShowCart
...     price_calc = DiscountCalc
...
...     @operation
...     def get(show_cart, pk):
...         return show_cart.show(cart_id=pk)

```

You can see that instead of classic Django class-based view we found
injector subclass with `view` decorator applied to it. `view` decorator
keeps your injector as it is except one thing. It adds `as_view`
function to its scope. This function returns an actual class-based view
instance ready to dispatch request.

The request will be dispatched based on it’s HTTP method. To process any
HTTP verb injector should contain a callable attribute named the same
way. Following verbs are supported `get`, `post`, `put`, `patch`,
`delete`, `head`, `options`, `trace`. This callable should take no
parameters. Everything it needs to work should be its dependency.
`operation` decorator is an excellent candidate for this.

Now let's take a look into actual business logic representation.

```pycon

>>> # cart/commands.py

>>> class ShowCart:
...     def __init__(self, price_calc):
...         pass
...
...     def show(self, cart_id):
...         pass

>>> class DiscountCalc:
...     pass

```

### Available scope

Dependency injecting happens before request processing. `view` decorator
takes a responsibility to populate injection scope with information
related to the current request.

- `view` actual class-based view instance processing request.
- `request` current request. First view function argument.
- `args` view positional arguments taken from url. This is a result of
  path converters application or regular expression non-named groups
  taken from an actual URL.
- `kwargs` view keyword arguments.
- `user` current user is taken from request. A short cat for
  frequently used request attribute.
- `pk` primary key view argument. A short cat for frequently used
  keyword argument.

## Template views

If you need to render template as a response to the request, you can
define template view. The main difference from the original
`TemplateView` subclass of the Django generics is the ability to use
dependency injection for things which will populate additional
template context.

```pycon
>>> # cart/views.py

>>> from dependencies import Injector, value
>>> from dependencies.contrib.django import template_view

>>> from examples.cart.commands import DiscountCalc

>>> @template_view
... class ShowCartWithDiscount(Injector):
...
...     # Template name with {{ price }} variable in it.
...     template_name = 'carts/discount.html'
...
...     price_calc = DiscountCalc
...
...     @value
...     def extra_context(price_calc, user):
...
...         return {'price': price_calc.calculate(user)}

```

You can pass following attributes to the injector subclass to
customize actual template render behavior.

- `template_name` view template name to render form on GET.
- `template_engine` alias of the configured template engine from the
  TEMPLATES setting.
- `response_class` HTTP response class to use.
- `content_type` response content type to use.
- `extra_context` extra context dict for template render.

### Available scope

Exactly the same as operations under HTTP verbs in the `@view`.

## Form processing views

Form processing views are similar to regular views in case of
definition.

```pycon

>>> # cart/views.py

>>> from dependencies import Injector, this
>>> from dependencies.contrib.django import form_view
>>> from examples.cart.commands import AddItem
>>> from examples.cart.forms import CartForm

>>> @form_view
... class AddCartItem(Injector):
...
...     # Attributes usual to the FormView to setup view behavior.
...     form_class = CartForm
...     template_name = 'carts/add_item.html'
...     success_url = '/purchase_complete/'
...
...     # Form Handling callbacks.
...     form_valid = this.command.process
...     form_invalid = this.command.show_error
...     command = AddItem
...
...     # Optional data decomposition.
...     item_name = this.form.cleaned_data['item_name']
...     order_id = this.form.cleaned_data['order_id']

```

`form_valid` and `form_valid` are two entry points for processing data.
Each attribute should be resolved to callable which takes no arguments.
If you need additional data for processing, use dependency injection to
pass them.

You can pass following attributes to the injector subclass to customize
actual form instance behavior.

- `form_class` actual Form class for data validation.
- `template_name` view template name to render form on GET.
- `success_url` url to be redirected after form valid callback. Can be
  a `reverse_lazy` instance.
- `template_engine` alias of the configured template engine from the
  TEMPLATES setting.
- `response_class` HTTP response class to use.
- `content_type` response content type to use.
- `initial` initial form data dict.
- `prefix` form prefix. Used in the HTML form representation in input
  names.
- `extra_context` extra context dict for template render.

### Available scope

In addition to the class based view scope extension, form processing
callbacks can use following dependencies.

- `form` actual form instance with data and files from
  request. `is_valid` method was already called.

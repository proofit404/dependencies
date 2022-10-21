# Mixins considered harmful

`dependencies` are compared with mixins often, since both solutions are ways to
maximize code reuse. We already discussed this in the [why](why.md#mixins)
chapter. But let's return to it again:

!!! note

    Inheritance always breaks encapsulation.

Mixin class depends on attributes set in other classes.

Consider this code snippet:

```pycon

>>> class RetrieveModelMixin:
...     """
...     Retrieve a model instance.
...     """
...
...     def retrieve(self, request, *args, **kwargs):
...         instance = self.get_object()
...         serializer = self.get_serializer(instance)
...         return Response(serializer.data)

```

Where were `get_object` and `get_serializer` defined? We have no idea. We
believe the code below is way better in the sense of understandability:

```pycon

>>> class RetrieveModel:
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

<p align="center">&mdash; ⭐ &mdash;</p>

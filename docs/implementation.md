# Internals

There a lot of magic under the hood of this library. Metaclasses, dunder
methods and `inspect` module all flying around.

When you define a class inherited from `Injector`:

1. Metaclass walks through all attributes defined in the class.
2. If an attribute is a `class`, we use `inspect` to analyse its
   constructor and make note of the spec of its dependencies.
3. At the end, it checks for circle links in the definition of the
   constructors, to protect you from infinite recursion.

When you access an attribute of the class inherited from `Injector`:

1. **getattr** defined in the class (with metaclass) looks for the attribute value.
2. If the value is not a class, it is returned as is.
3. If it is a class, the metaclass looks for its spec. In the loop, it tries to
   resolve each of constructor's arguments to match the spec, until all attributes
   are resolved.
4. If a found attribute is a class, we call **getattr** again looking for its spec
   in the same loop without recursion.

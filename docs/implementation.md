# Internals

There a lot of magic under the hood of this library. Metaclasses, dunder
methods and `inspect` module all flying around.

When you define a class inherited from `Injector`:

1. Metaclass walks through all attributes defined in the class.
2. If attribute is a class, it `inspect` it's constructor and record
   the spec of it's dependencies.
3. At the end it check for circle links in the definition of the
   constructors to protect you from infinite recursion.

When you access attribute of the class inherited from `Injector`

1. **getattr** defined in the class (with metaclass) looking for a
   spec.
2. If it is not a class, attribute returned as is.
3. If it is a class, it looking for its spec. In the loop it tries to
   resolve it's attributes to match the spec until all attributes
   found.
4. If found attribute is a class to **getattr** looking for its spec
   in the same loop without recursion.

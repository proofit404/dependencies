# Sticky scopes

## Why

Sometimes we need to touch multiple objects within the composition. The most
common example could be a decorator pattern from OOP books. Let say we have an
object which will touch the database couple of times during it's method
execution. Service objects could easily do that. Of course, we would not couple
service object with concrete database access implementation. We would use
inversion of control to inject those queries into service object via its
constructor.

Service objects could be easily contains another service objects to delegate
business logic of lower levels to nested services. Let say we would like to
manage database access on per service basis. Each service including nested ones
should run its queries in a separate database transaction. How would we handle
that?

### Decorator pattern

Let say we having a structure like that:

```pycon

>>> from dependencies import Injector
>>> from app.services import Root, NestedA, NestedB, NestedC
>>> from app.transactions import Transactional

>>> class Container(Injector):
...     root = Root
...     nested_a = Transactional
...     service = NestedA
...     nested_b = NestedB
...     nested_c = NestedC

>>> Container.root
Root(Transactional(NestedA()), NestedB(), NestedC())

```

Now the question would be - how do you access inner transactional objects to
check its state or trigger a rollback?

### Inner object access

First of all we need to remember that each attribute access on `Injector`
subclass would create a new compositions of new objects.

```pycon

>>> Container.root.do()

>>> Container.nested_a.commit()
FAIL

```

The second line above created new `NestedA` instance with fresh state. That's
why transaction failed.

We could store a concrete composition instance in the variable and access inner
objects to check their state.

```pycon

>>> root = Container.root

>>> root.do()

>>> root.nested_a.commit()
DONE

```

Code above didn't create new objects, that's why transaction was handled
properly. But code above has a lot of design problems:

- It forces client code to depend on inner structure of objects beyond their
  interfaces
- Objects could protect its inner structures (with libraries like
  [generics](https://proofit404.github.io/generics/))
- Every time we would try to refactor implementation details of the called
  code - client code would break

## Principles

- [Sticky scopes remember instances](#sticky-scopes-remember-instances)

### Sticky scopes remember instances

`Injector` subclasses could be used as context managers to create sticky scopes.
Sticky scopes would creates objects once. You would be able to access different
objects from the same composition.

```pycon

>>> with Container as scope:
...     scope.root.do()
...     scope.nested_a.commit()
DONE

```

As you may notice objects stays the same:

```pycon

>>> with Container as scope:
...     scope.root is scope.root
True

```

<p align="center">&mdash; ⭐ &mdash;</p>
<p align="center"><i>The <code>dependencies</code> library is part of the SOLID python family.</i></p>

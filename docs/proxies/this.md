# `this` proxy

`this` is a declarative way to access attributes and items of other
dependencies defined in the `Injector` subclasses. The Link is basically
a pointer or an alias to another dependency in the same `Injector`, in
nested `Injector` or in parent `Injector`.

```pycon

>>> from dependencies import Injector, this

```

## Simple links

For example, you can create simple aliases.

```pycon

>>> class Container(Injector):
...     foo = 1
...     bar = this.foo

>>> Container.bar
1

```

You can use item access on dependencies defined in `Injector` subclass.

```pycon

>>> class Container(Injector):
...     foo = {'a': 1}
...     bar = this.foo['a']

>>> Container.bar
1

```

Tuple, list, set and everything that supports iterable protocol are also
supported.

You can use this links as usual in the constructor arguments.

```pycon

>>> class Foo:
...     def __init__(self, bar):
...         self.bar = bar

>>> class Container(Injector):
...     foo = Foo
...     bar = this.baz
...     baz = 1

>>> Container.foo.bar
1

```

Also, you can see, that you can define proxy a before the actual
dependency it pointing to.

You can point a link to the instance method. The actual instance will be
built before resolving method access. This is a useful technique to hide
whole class with its own state behind a single callable interface.

```pycon

>>> class Foo:
...     def method(self, arg):
...         print(self)
...         print(arg)

>>> class Container(Injector):
...     foo = Foo
...     bar = this.foo.method

>>> Container.bar(1)  # doctest: +ELLIPSIS
<__main__.Foo object at 0x...>
1

```

You can see that `method` has access to the `Foo` instance. So it can
call other methods of `Foo`. You can define dependencies of the `Foo`
class in it constructor as usual.

## Nested and parent injector access

Links created with `this` objects can access attributes defined in the
nested injector.

```pycon

>>> class Container(Injector):
...     foo = this.Bar.baz.__add__
...     class Bar(Injector):
...         baz = 1

>>> Container.foo(2)
3

```

Nested `Injector` subclasses **can** access attributes of the parent
`Injector`. Use left shift operator to specify the number of levels to
go upper scope.

```pycon

>>> class Container(Injector):
...     foo = 1
...     class Bar(Injector):
...         baz = (this << 1).foo.__add__

>>> Container.Bar.baz(2)
3

```

## Full example

Let's define an application with all settings stored in the dictionary.
In production, you can substitute this dictionary with Consul or
ZooKeeper client and the rest of the application will be left untouched.

```pycon

>>> class Database:
...     def __init__(self, host, port):
...         self.host = host
...         self.port = port

>>> class Cache:
...     def __init__(self, host, port):
...         self.host = host
...         self.port = port

>>> class Application:
...     def __init__(self, db, cache):
...         self.db = db
...         self.cache = cache

>>> class Container(Injector):
...     app = Application
...     db = this.DB.database
...     cache = this.InMemory.cache
...
...     class DB(Injector):
...         database = Database
...         host = (this << 1).settings['database']['host']
...         port = (this << 1).settings['database']['port']
...
...     class InMemory(Injector):
...         cache = Cache
...         host = (this << 1).settings['cache']['host']
...         port = (this << 1).settings['cache']['port']
...
...     settings = {
...         'database': {
...             'host': 'localhost',
...             'port': 5432,
...         },
...         'cache': {
...             'host': 'localhost',
...             'port': 6782,
...         },
...     }

>>> Container.app  # doctest: +ELLIPSIS
<__main__.Application object at 0x...>

>>> Container.app.db  # doctest: +ELLIPSIS
<__main__.Database object at 0x...>

>>> Container.app.db.port
5432

>>> Container.app.cache  # doctest: +ELLIPSIS
<__main__.Cache object at 0x...>

>>> Container.app.cache.port
6782

```

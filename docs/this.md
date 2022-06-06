# `this` object

`this` is a declarative way to access attributes and items of other dependencies
defined in the `Injector` subclasses. The Link is basically a pointer or an
alias to another dependency in the same `Injector`, in nested `Injector` or in
parent `Injector`.

```pycon

>>> from dependencies import Injector, this

>>> class Main:
...     def __init__(self, result):
...         self.result = result

```

## Simple links

For example, you can create simple aliases.

```pycon

>>> class Container(Injector):
...     main = Main
...     result = this.foo
...     foo = 1

>>> Container.main.result
1

```

You can use item access on dependencies defined in `Injector` subclass.

```pycon

>>> class Container(Injector):
...     main = Main
...     result = this.foo['a']
...     foo = {'a': 1}

>>> Container.main.result
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

You may notice that it is possible to define `this` object before the dependency
it point to.

You can point a link to the instance method. The actual instance will be built
before resolving method access. This is a useful technique to hide whole class
with its own state behind a single callable interface.

```pycon

>>> class Foo:
...     def method(self, arg):
...         print(self)
...         print(arg)

>>> class Container(Injector):
...     main = Main
...     result = this.foo.method
...     foo = Foo

>>> Container.main.result(1)  # doctest: +ELLIPSIS
<__main__.Foo object at 0x...>
1

```

You can see that `method` has access to the `Foo` instance. It can call other
methods of `Foo`. You can define dependencies of the `Foo` class in it
constructor as usual.

## Nested `Injector` access

It is possible to inject `Injector` itself. `Injector` subclasses are provided
as is, and calculate their attributes on first use.

Links created with `this` objects can access attributes defined in the nested
injector.

```pycon

>>> class Container(Injector):
...     main = Main
...     result = this.Bar.baz.__add__
...
...     class Bar(Injector):
...         baz = 1

>>> Container.main.result(2)
3

```

Nested `Injector` subclasses **can** access attributes of the parent `Injector`.
Use left shift operator to specify the number of levels to go upper scope.

```pycon

>>> class Container(Injector):
...     main = Main
...     result = this.Bar.baz
...     foo = 1
...
...     class Bar(Injector):
...         baz = (this << 1).foo.__add__

>>> Container.main.result(2)
3

```

## Full example

Let's define an application with all settings stored in the dictionary. In
production, you can substitute this dictionary with Consul or ZooKeeper client
and the rest of the application will be left untouched.

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

>>> isinstance(Container.app, Application)
True

>>> isinstance(Container.app.db, Database)
True

>>> Container.app.db.port
5432

>>> isinstance(Container.app.cache, Cache)
True

>>> Container.app.cache.port
6782

```

## Environment variables

It is possible to access environment variables during dependency injection
process. If a class has a dependency in it's constructor, you can pass a value
from environment variable to the constructor using `this` object.

```pycon

>>> import os

>>> class App:
...
...     def __init__(self, config):
...
...         self.config = config
...
...     def __repr__(self):
...
...         return f'App({self.config!r})'

>>> class Config:
...
...     def __init__(self, frontend_url, backend_url):
...
...         self.frontend_url = frontend_url
...         self.backend_url = backend_url
...
...     def __repr__(self):
...
...         return f'Config({self.frontend_url!r}, {self.backend_url!r})'

>>> class Container(Injector):
...
...     app = App
...     config = Config
...     frontend_url = this.environ['FRONTEND_URL']
...     backend_url = this.environ['BACKEND_URL']
...     environ = os.environ

>>> Container.app
App(Config('https://example.com/frontend', 'https://example.com/backend'))

```

<p align="center">&mdash; ⭐ &mdash;</p>

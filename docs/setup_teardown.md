# Setup and teardown

## Why

It is a common sittuation that you would need a little bit of logic before
building your objects and a little bit of logic after you use built objects. Let
say, connection pool needs to be initialized before you could properly use your
service objects. The same connection pool should be shutdown correctly after
your service object done with its part. Of course, connection pool is a
noticeable example of a general resource management problem.

### Hidden complexity

In complex frameworks like object relation mappers usually all complexity of
resource management is hidden by development API. Often you would use let say a
database model and didn't even notice that connection to the database was made,
or database transaction was started.

```pycon

>>> from app.models import Report

>>> Report.objects.select()
[<Report: 1>, <Report: 2>, <Report: 3>]

```

This is a convenient approach to access data source you are interested in. And
developers how designed framework API in such way done a greet job to simplify
lives of their software users.

And what we would do in case there is no such library for a data source we would
like to communicate with? What we gonna do in that case? Should we spend endless
time crafting such library for ourselves?

For example, we need to integrate our application with a third-party service
over ther JSON API. And developers of this third-party service didn't bother to
write a proper client library for python. Should we pollute our business objects
with knowledge of HTTP keep-alive management? It should be a better place for
such low-level logic.

## Principles

- [`@value` object could `yield` value](#value-object-could-yield-value)
- [Teardown happens in opposite order to setup](#teardown-happens-in-opposite-order-to-setup)

### `@value` object could `yield` value

When you use `Injector` subclasses as context managers it allows you to write
setup and teardown logic inside evaluated dependencies. `@value` object could be
a generator function. Setup code would be executed before `yield` statement. An
object returned by `yield` statement would be injected as an argument matching
generator function name. When the code would leave `with` statement block the
rest of the generator would be executed to the end of function. You could put a
tear down logic in this place.

```pycon

>>> from dependencies import Injector, value
>>> from requests import Session
>>> from dataclasses import dataclass

>>> @dataclass
... class Account:
...     http: Session
...
...     def suspend(self, user_id):
...         user = self.http.get(f"http://api.com/users/{user_id}/")
...         for group_id in user.json()["groups"]:
...             self.http.delete(f"http://api.com/groups/{group_id}/members/{user_id}/")

>>> class App(Injector):
...     account = Account
...
...     @value
...     def http():
...         with Session() as session:
...             yield session

>>> with App as app:
...     app.account.suspend(142)
...     app.account.suspend(318)

```

!!! note

    A wise reader would notice that [sticky scopes](./sticky.md) rules are
    applied. In both calls `account` would share the same `Account`
    instance which share the same `Session` instance which was initiated
    only once. That's mean both business object calls would use same
    keep-alive TCP connection.

It's a similar approach that `pytest` project takes with it's
[fixtures](https://docs.pytest.org/en/latest/how-to/fixtures.html#yield-fixtures-recommended).

### Teardown happens in opposite order to setup

As we mention previously, setup and teardown logic usually used to do side
effects. The order in which you do side effect is not the same in which you undo
side effects. A database transaction can't be committed or rollback after
database connection was destroyed.

For that purpose `dependencies` would execute teardown steps in exactly opposite
order to the setup steps. You could rely of this assumption during design of
your value objects internals. It's a contract guarantied by our API.

```pycon

>>> from app.database import Cursor, Connection

>>> @dataclass
... class Account:
...     cursor: Cursor
...
...     def suspend(self, nick):
...         self.cursor.select(name=nick).delete()


>>> class App(Injector):
...     account = Account
...
...     @value
...     def cursor(connection):
...         cur = Cursor(connection)
...         cur.begin_transaction()
...         yield cur
...         cur.commit_transaction()
...
...     @value
...     def connection():
...         db = Connection()
...         db.connect()
...         yield db
...         db.disconnect()

>>> with App as app:
...     app.account.suspend('Jeff')
CONNECT TO production;
BEGIN TRANSACTION;
SELECT * FROM users FOR UPDATE;
DELETE FROM users;
COMMIT TRANSACTION;
DISCONNECT FROM production;

```

<p align="center">&mdash; ⭐ &mdash;</p>

# What to inject, and what not to

It can be hard to draw the border between what should be injectable and what
shouldn't be. Let's consider this typical example.

```pycon

>>> import requests
>>> import dependencies

>>> class UserGetter:
...     def __init__(self, http):
...         self.http = http
...
...     def __call__(self, user_id):
...         return self.http.get("http://api.com/users/%d/" % (user_id,)).json()

>>> class Users(dependencies.Injector):
...
...     get = UserGetter
...     http = requests

>>> Users.get(1)
{'id': 1, 'name': 'John', 'surname': 'Doe'}

```

1. Should I write code like this?
2. Will I ever decide to use something other than the excellent
   [requests](http://docs.python-requests.org/) library?

In our opinion these are not the correct questions to ask.

By injecting a certain library you add a **hard** dependency on its interfaces
to the whole system. Migration to other libraries in the future can be painful.

Also, this adds another **hard** dependency to the whole system. Your code
depends on the structure of third-party API response. This makes the situation
even worse. Migration to other third-party services will be painful, as well.

We believe that HTTP protocol itself is an implementation detail!

We prefer to use dependency injection only on boundaries we control:

```pycon

>>> import dataclasses
>>> import dependencies
>>> import requests

>>> class HomePage:
...
...     def __init__(self, get_user):
...         self.get_user = get_user
...
...     def show(self, user_id):
...         user = self.get_user(user_id=user_id)

>>> @dataclasses.dataclass
... class UserStruct:
...
...     id: int
...     name: str
...     surname: str

>>> def get_user(user_id):
...
...     response = requests.get("http://api.com/users/%d/" % (user_id,))
...     return UserStruct(**response.json())

>>> class Site(dependencies.Injector):
...
...     home_page = HomePage
...     get_user = get_user

>>> Site.home_page.show(1)

```

<p align="center">&mdash; ⭐ &mdash;</p>

# Reading configuration

An application with proper architecture has plugable configuration which is easy
to tune according to changing environment, like servers, DNS names, and
orchestration strategies.

Most of the time you would use a framework like Django, Flask, or FastAPI as
foundation for your infrastructure (implementation details) layer. These
frameworks tend to provide configuration instruments like Django settings file,
Flask application factory, and so on.

These defaults could serve you needs so far, but in more complex applications
which includes a lot of moving parts such approach could hit design limations
pretty soon.

`dependencies` library draw the border between your infrastructure layer and
your business domain. The way you configure your application is implementation
detail itself.

## Principles

- [Hard-coded configuration](#hard-coded-configuration)
- [Reading configuration file](#reading-configuration-file)
- [Reading environment variables](#reading-environment-variables)
- [Reading settings from network](#reading-settings-from-network)

### Hard-coded configuration

Most easiest and straightforward way to define project settings is to hardcode
it inside application `Injector` subclass. Such approach would work nice during
proof of concept development stage. Early in the development days you would
probably more focused on business idea itself rather environment it would run
inside.

```pycon

>>> from dependencies import Injector, this
>>> from application import App, PostgreSQL, Redis

>>> class Container1(Injector):
...     app = App
...     database = this.Database.connection
...     cache = this.Cache.connection
...
...     class Database(Injector):
...         connection = PostgreSQL
...         host = (this << 1).settings["postgresql"]["host"]
...         port = (this << 1).settings["postgresql"]["port"]
...
...     class Cache(Injector):
...         connection = Redis
...         host = (this << 1).settings["redis"]["host"]
...         port = (this << 1).settings["redis"]["port"]
...
...     settings = {
...         "postgresql": {
...             "host": "localhost",
...             "port": 5432,
...         },
...         "redis": {
...             "host": "localhost",
...             "port": 6379,
...         },
...     }

>>> Container1.app.run()
Connecting to localhost:5432
Connecting to localhost:6379

```

### Reading configuration file

For simple deployments configuration file would be an obvious choice. Let say
you have this file somewhere in your `/etc` folder on your server.

```yml
---
postgresql:
  host: 127.0.0.3
  port: 5432
redis:
  host: 127.0.0.3
  port: 6379
```

We could create a singleton configuration instance. File would be read only
once.

```pycon

>>> from functools import lru_cache
>>> from dependencies import Injector, this, value
>>> from yaml import safe_load
>>> from application import App, PostgreSQL, Redis

>>> class Container2(Injector):
...     app = App
...     database = this.Database.connection
...     cache = this.Cache.connection
...
...     class Database(Injector):
...         connection = PostgreSQL
...         host = (this << 1).settings["postgresql"]["host"]
...         port = (this << 1).settings["postgresql"]["port"]
...
...     class Cache(Injector):
...         connection = Redis
...         host = (this << 1).settings["redis"]["host"]
...         port = (this << 1).settings["redis"]["port"]
...
...     @value
...     @lru_cache
...     def settings(config):
...         with open(config) as f:
...             return safe_load(f)
...
...     config = "docs/config.yml"

>>> Container2.app.run()
Connecting to 127.0.0.3:5432
Connecting to 127.0.0.3:6379

```

As you may notice the only thing that changed was `settings` definition and its
dependency with path to the file. That make it obvious we could define
application container by reusing our first definition with hardcoded settings.

```pycon

>>> from functools import lru_cache
>>> from dependencies import this, value
>>> from yaml import safe_load

>>> class Container3(Container1):
...     @value
...     @lru_cache
...     def settings(config):
...         with open(config) as f:
...             return safe_load(f)
...
...     config = "docs/config.yml"

>>> Container2.app.run()
Connecting to 127.0.0.3:5432
Connecting to 127.0.0.3:6379

```

### Reading environment variables

Some deployment options makes it hard to create configuration files on the
target host system. [Heroku](https://www.heroku.com/) advertise its
twelve-factor application approach heavily. Sometimes environment variables
would be an option. But consider it a security risk.

```pycon

>>> from os import environ
>>> from dependencies import Injector, this, value
>>> from application import App, PostgreSQL, Redis

>>> class Container(Injector):
...     app = App
...     database = this.Database.connection
...     cache = this.Cache.connection
...
...     class Database(Injector):
...         connection = PostgreSQL
...         host = (this << 1).settings["postgresql"]["host"]
...         port = (this << 1).settings["postgresql"]["port"]
...
...     class Cache(Injector):
...         connection = Redis
...         host = (this << 1).settings["redis"]["host"]
...         port = (this << 1).settings["redis"]["port"]
...
...     @value
...     def settings():
...         return {
...             "postgresql": {
...                 "host": environ["POSTGRESQL_HOST"],
...                 "port": environ["POSTGRESQL_PORT"],
...             },
...             "redis": {
...                 "host": environ["REDIS_HOST"],
...                 "port": environ["REDIS_PORT"],
...             },
...         }

>>> Container.app.run()
Connecting to postgresql-instance1.cg034hpkmmjt.us-east-1.rds.amazonaws.com:5432
Connecting to redis-01.7abc2d.0001.usw2.cache.amazonaws.com:6379

```

### Reading settings from network

A best option for solid deployment setup would be some variant of service
discovery platform.

You could conside combination of HashiCorp
[Consul](https://www.hashicorp.com/products/consul) and
[Vault](https://www.hashicorp.com/products/vault) the editors choice.

We discover database and cache host using consul client. After that we request a
password for found service from vault. Optionaly, we could configure consul
client using environment variables. Let say we could change default port for
local consul agent.

```pycon

>>> from functools import lru_cache
>>> from consul import Consul
>>> from dependencies import Injector, this
>>> from application import App, PostgreSQL, Redis

>>> class Container(Injector):
...     app = App
...     database = this.Database.connection
...     cache = this.Cache.connection
...
...     class Database(Injector):
...         connection = PostgreSQL
...         host = (this << 1).settings["postgresql"]["host"]
...         port = (this << 1).settings["postgresql"]["port"]
...
...     class Cache(Injector):
...         connection = Redis
...         host = (this << 1).settings["redis"]["host"]
...         port = (this << 1).settings["redis"]["port"]
...
...     @value
...     @lru_cache
...     def settings(consul):
...         return {
...             "postgresql": {
...                 "host": consul.kv.get("postgresql_host")[1]["Value"],
...                 "port": consul.kv.get("postgresql_port")[1]["Value"],
...             },
...             "redis": {
...                 "host": consul.kv.get("redis_host")[1]["Value"],
...                 "port": consul.kv.get("redis_port")[1]["Value"],
...             },
...         }
...
...     consul = Consul

>>> Container.app.run()
Connecting to local consul agent
Connecting to postgresql-instance1.cg034hpkmmjt.us-east-1.rds.amazonaws.com:5432
Connecting to redis-01.7abc2d.0001.usw2.cache.amazonaws.com:6379

```

<p align="center">&mdash; ⭐ &mdash;</p>

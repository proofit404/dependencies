================
 ``this`` proxy
================

You can create link in your ``Injector`` subclasses.  Proxy is
basically a pointer or an alias to another dependency in the same
``Injector``, in nested ``Injector`` or in parent ``Injector``.

.. code:: python

    >>> class Database(object):
    ...     def __init__(self, host, port):
    ...         self.host = host
    ...         self.port = port
    ...
    >>> class Cache(object):
    ...     def __init__(self, host, port):
    ...         self.host = host
    ...         self.port = port
    ...
    >>> class Application(object):
    ...     def __init__(self, db, cache):
    ...         self.db = db
    ...         self.cache = cache
    ...
    >>> from dependencies import Injector, this
    >>> class Scope(Injector):
    ...     app = Application
    ...     db = this.DB.database
    ...     cache = this.InMemory.cache
    ...     class DB(Injector):
    ...         database = Database
    ...         host = (this << 1).settings['database']['host']
    ...         port = (this << 1).settings['database']['port']
    ...     class InMemory(Injector):
    ...         cache = Cache
    ...         host = (this << 1).settings['cache']['host']
    ...         port = (this << 1).settings['cache']['port']
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
    ...
    >>> Scope.app.db.port
    5432
    >>> Scope.app.cache.port
    6782
    >>>

You can use ``this`` object as a special pointer where to start.
Place ``this`` object at the injector attribute, which must be
injected from somewhere else.  When you will try to access this
attribute, ``Injector`` will take actual instance from attribute and
item access of the injection scope.  You can point attribute to the
outer ``Injector`` attribute with the left shift operator.

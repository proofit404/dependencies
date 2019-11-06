# Celery contrib

[Celery](http://www.celeryproject.org/) is a well known distributed task
queue for Python. The task is the main abstraction you work with in
Celery. Dependencies provide a way to define shared and regular tasks
directly from injector subclasses. So you can `delay` them as usual
tasks.

## Define a task

To define a task from the injector use `task` decorator.

```pycon

>>> from celery import Celery
>>> from dependencies import Injector
>>> from dependencies.contrib.celery import task

>>> class SayHello:
...
...     def __init__(self, args):
...         self.args = args
...
...     def __call__(self):
...         return 'Hello %s.' % self.args[0]

>>> celery = Celery('hello')
>>> celery.conf.update({'task_always_eager': True})

>>> @task
... class HelloTask(Injector):
...
...     app = celery
...     name = 'hello'
...     run = SayHello

>>> HelloTask.delay('world').get()
'Hello world.'

```

In this example, we define a regular
[Celery](http://www.celeryproject.org/) task from the injector subclass.
When worker got it, it will build `SayHello` instance, get it bound
`__call__` method and call it.

### Customizable arguments

This attributes can be defined on the injector subclass to tweak the
behavior of the celery task instance.

- `app` is the actual celery instance where the task will be
  registered. Optional for shared tasks (see below).
- `name` of the registered task.
- `run` should be resolved to the callable with takes no
  arguments. Arguments passed to the `delay` or `apply_async` are
  available in the injector scope. Use DI to access them.
- `base_class` base class of the task. Customize it in the case you
  want to define your own `on_failure` handler.
- `bind` creates a bound task. Task instance will be available in the
  scope under the `task` name.
- `typing`
- `max_retries`
- `default_retry_delay`
- `rate_limit`
- `ignore_result`
- `trail`
- `send_events`
- `store_errors_even_if_ignored`
- `serializer`
- `time_limit`
- `soft_time_limit`
- `track_started`
- `acks_late`
- `reject_on_worker_lost`
- `throws`

Attributes without explicit comments behave exactly as `@app.task`
decorator arguments. See [Celery](http://www.celeryproject.org/)
documentation for more info.

### Available scope

Before running task in the worker, the scope of the injector will be
extended with this attributes.

- `task` the actual task instance in the case of bound
  tasks. Unavailable otherwise.
- `args` positional arguments of the `delay` call.
- `kwargs` keyword arguments of the `delay` call.

## Define shared task

It is also possible to define shared tasks if you don't have access to
the instance of the celery application. For example, you are using
Celery together with Django.

```pycon

>>> # order/tasks.py

>>> from celery import canvas
>>> from dependencies.contrib.celery import shared_task
>>> from examples.order.commands import ProcessOrder

>>> @shared_task
... class ProcessOrderTask(Injector):
...
...     name = 'process_order'
...     run = ProcessOrder

>>> ProcessOrderTask.delay()  # doctest: +ELLIPSIS
<EagerResult: ...>

```

As you can see, there is no need for the actual application instance.

## Retry tasks

[Celery](http://www.celeryproject.org/) offers you bound tasks for the
purpose of retrying the same task few times. Bind if you decide to use
dependency injection, you probably don't want your business objects to
know about implementation details such as task queues, wsgi frameworks,
etc.

But with `dependencies`, you can use the bound task in a clean way
without abusing your business logic with implementation details.

```pycon

>>> # order/commands.py

>>> class ProcessOrder:
...
...     def __init__(self, retry):
...         self.retry = retry
...
...     def __call__(self):
...         self.retry()

>>> # order/tasks.py

>>> from dependencies import Injector, this
>>> from dependencies.contrib.celery import shared_task
>>> from examples.order.commands import ProcessOrder

>>> @shared_task
... class ProcessOrderTask(Injector):
...
...     name = 'process_order'
...     run = ProcessOrder
...
...     bind = True
...     retry = this.task.retry

```

## Using Canvas

Usually, you schedule tasks somewhere in your own code. Calling
`task.delay()` method is the most common way to do that. It is also
available for tasks defined with dependencies contrib.

```pycon

>>> from examples.order.tasks import ProcessOrderTask

>>> # Delay injector.
>>> ProcessOrderTask.delay(1, 2)  # doctest: +ELLIPSIS
<EagerResult: ...>

```

So dependencies contrib comes with an easy way to define canvas using
injector attributes.

```pycon

>>> from examples.order.tasks import ProcessOrderTask

>>> # Shortcut using star arguments.
>>> ProcessOrderTask.s(1, 2).delay()  # doctest: +ELLIPSIS
<EagerResult: ...>

>>> # Immutable shortcut using star arguments.
>>> ProcessOrderTask.si(1, 2).delay()  # doctest: +ELLIPSIS
<EagerResult: ...>

>>> # Complete signature.
>>> ProcessOrderTask.signature(args=(1, 2)).delay()  # doctest: +ELLIPSIS
<EagerResult: ...>

```

It is also possible to decouple business logic which should delay a task
from knowing this is a task.

```pycon

>>> # order/views.py

>>> from dependencies import Injector, this
>>> from examples.order.tasks import ProcessOrderTask

>>> class SubmitOrderView(Injector):
...
...     schedule_payment = this.payment.delay
...     payment = ProcessOrderTask

```

In this case, your business logic can use `schedule_payment` as a
regular function without knowing anything about task queues.

from dependencies import Injector
from dependencies import this
from dependencies.contrib.celery import shared_task
from examples.order.commands import ProcessOrder


@shared_task
class ProcessOrderTask(Injector):
    name = "process_order"
    run = ProcessOrder
    bind = True
    retry = this.task.retry

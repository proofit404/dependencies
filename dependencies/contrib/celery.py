"""
dependencies.contrib.celery
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements injectable Celery task.

:copyright: (c) 2016-2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

from ._celery import shared_task, task

__all__ = ["shared_task", "task"]

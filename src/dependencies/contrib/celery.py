"""
dependencies.contrib.celery
---------------------------

This module implements injectable Celery task.

:copyright: (c) 2016-2020 by dry-python team.
:license: BSD, see LICENSE for more details.
"""
from _dependencies.contrib.celery import shared_task
from _dependencies.contrib.celery import task


__all__ = ["shared_task", "task"]

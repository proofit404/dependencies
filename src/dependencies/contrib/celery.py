"""
dependencies.contrib.celery
---------------------------

This module implements injectable Celery task.

:copyright: (c) 2016-2019 by dry-python team.
:license: BSD, see LICENSE for more details.
"""

from ._celery import shared_task, task


__all__ = ["shared_task", "task"]

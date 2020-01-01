"""
dependencies.contrib.django
---------------------------

This module implements injectable Django view.

:copyright: (c) 2016-2020 by dry-python team.
:license: BSD, see LICENSE for more details.
"""
from _dependencies.contrib.django import form_view
from _dependencies.contrib.django import template_view
from _dependencies.contrib.django import view


__all__ = ["form_view", "template_view", "view"]

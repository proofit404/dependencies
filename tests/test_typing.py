# -*- coding: utf-8 -*-
"""Tests related to compatibility with standard typing python module."""
import pytest

from dependencies import Injector

typing = pytest.importorskip("typing")


typing.Type[Injector]

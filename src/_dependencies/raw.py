# -*- coding: utf-8 -*-
from _dependencies.markers import injectable


def _make_raw_spec(dependency):

    return injectable, _RawSpec(dependency), [], 0


class _RawSpec(object):
    def __init__(self, dependency):

        self.dependency = dependency

    def __call__(self):

        return self.dependency

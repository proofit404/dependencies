# -*- coding: utf-8 -*-
import doctest
import sys
from doctest import testfile
from glob import glob

import responses
from django.apps import apps
from django.conf import settings


def _setup():
    apps.populate(settings.INSTALLED_APPS)
    responses.add(
        responses.GET,
        "http://api.com/users/1/",
        json={"id": 1, "name": "John", "surname": "Doe"},
    )
    responses.start()


def _advanced_test():
    import doctested_module

    doctest.testmod(doctested_module)


def _main():
    markdown_files = glob("**/*.md", recursive=True)
    exit_code = 0
    for markdown_file in markdown_files:
        failed, attempted = testfile(markdown_file, module_relative=False)
        exit_code += failed
    sys.exit(exit_code)


if __name__ == "__main__":
    _setup()
    _advanced_test()
    _main()

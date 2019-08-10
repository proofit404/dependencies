import sys
from doctest import testfile
from glob import glob

import responses
from django.apps import apps
from django.conf import settings


def main():
    apps.populate(settings.INSTALLED_APPS)
    responses.add(
        responses.GET,
        "http://api.com/users/1/",
        json={"id": 1, "name": "John", "surname": "Doe"},
    )
    responses.start()
    markdown_files = glob("**/*.md", recursive=True)
    exit_code = 0
    for markdown_file in markdown_files:
        failed, attempted = testfile(markdown_file, module_relative=False)
        exit_code += failed
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

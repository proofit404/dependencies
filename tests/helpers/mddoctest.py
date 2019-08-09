import sys
from doctest import testfile
from glob import glob

from django.apps import apps
from django.conf import settings


def main():
    apps.populate(settings.INSTALLED_APPS)
    markdown_files = glob("**/*.md", recursive=True)
    exit_code = 0
    for markdown_file in markdown_files:
        failed, attempted = testfile(markdown_file, module_relative=False)
        exit_code += failed
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

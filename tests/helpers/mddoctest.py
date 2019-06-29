import sys
from doctest import testfile
from glob import glob


def main():
    markdown_files = glob("**/*.md", recursive=True)
    exit_code = 0
    for markdown_file in markdown_files:
        failed, attempted = testfile(markdown_file, module_relative=False)
        exit_code += failed
    sys.exit(exit_code)

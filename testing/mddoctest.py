from doctest import testfile
from glob import glob
from sys import exit


def _setup():
    from os import environ
    import responses

    environ["FRONTEND_URL"] = "https://example.com/frontend"
    environ["BACKEND_URL"] = "https://example.com/backend"
    responses.add(
        responses.GET,
        "http://api.com/users/1/",
        json={"id": 1, "name": "John", "surname": "Doe"},
    )
    responses.start()


def _main():
    exit_code = 0
    for markdown_file in glob("docs/**/*.md", recursive=True):
        failed, attempted = testfile(markdown_file, module_relative=False)
        exit_code += failed
    exit(exit_code)


if __name__ == "__main__":  # pragma: no branch
    _setup()
    _main()

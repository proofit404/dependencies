from doctest import testfile
from glob import glob
from sys import exit


def _setup():
    from os import environ
    import responses

    # This object examples.
    environ["FRONTEND_URL"] = "https://example.com/frontend"
    environ["BACKEND_URL"] = "https://example.com/backend"

    # Settings guide.
    environ[
        "POSTGRESQL_HOST"
    ] = "postgresql-instance1.cg034hpkmmjt.us-east-1.rds.amazonaws.com"
    environ["POSTGRESQL_PORT"] = "5432"
    environ["REDIS_HOST"] = "redis-01.7abc2d.0001.usw2.cache.amazonaws.com"
    environ["REDIS_PORT"] = "6379"

    # Setup and teardown examples.
    responses.add(responses.GET, "http://api.com/users/142/", json={"groups": [712]})
    responses.add(responses.GET, "http://api.com/users/318/", json={"groups": [905]})
    responses.add(responses.DELETE, "http://api.com/groups/712/members/142/")
    responses.add(responses.DELETE, "http://api.com/groups/905/members/318/")

    # FAQ examples.
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

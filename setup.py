from setuptools import setup


readme = open("README.rst").read() + open("CHANGELOG.rst").read()


setup(
    name="dependencies",
    version="0.15",
    description="Dependency Injection for Humans",
    long_description=readme,
    license="BSD",
    url="https://github.com/dry-python/dependencies",
    author="Artem Malyshev",
    author_email="proofit404@gmail.com",
    packages=["dependencies", "dependencies.contrib", "dependencies._checks"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development",
    ],
)

from setuptools import setup


setup(name="helpers", py_modules=["helpers"])

setup(name="pkg", packages=["pkg"])

setup(name="django_settings_module", py_modules=["django_settings_module"])

setup(
    name="polls",
    packages=["polls", "polls.api"],
    include_package_data=True,
    package_data={"polls": ["templates/*.html"]},
)

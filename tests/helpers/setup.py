from setuptools import setup


setup(name="helpers", py_modules=["helpers"])

setup(name="pkg", packages=["pkg"])

setup(
    name="django_project",
    packages=["django_project", "django_project.api"],
    include_package_data=True,
    package_data={"django_project": ["templates/*.html"]},
)

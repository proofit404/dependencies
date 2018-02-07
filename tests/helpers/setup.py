from setuptools import setup

setup(name='helpers', py_modules=['helpers'])

setup(name='django_settings_module', py_modules=['django_settings_module'])

setup(
    name='urlconfs',
    py_modules=[
        'urlconf_dispatch_request',
        'urlconf_inject_user',
        'urlconf_pass_kwargs_to_the_service',
        'urlconf_create_view',
    ],
)

setup(
    name='polls',
    packages=['polls', 'polls.migrations'],
    include_package_data=True,
    package_data={'polls': ['templates/polls/*.html']},
)

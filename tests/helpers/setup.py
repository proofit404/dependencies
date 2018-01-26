from setuptools import setup

setup(name='helpers', py_modules=['helpers'])

setup(name='django_settings_module', py_modules=['django_settings_module'])

setup(
    name='urlconfs',
    py_modules=[
        'urlconf_dispatch_request',
        'urlconf_inject_user',
    ],
)

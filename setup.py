from setuptools import setup

readme = open('README.rst').read() + open('CHANGELOG.rst').read()

setup(
    name='dependencies',
    version='0.13',
    description='Dependency Injection for Humans',
    long_description=readme,
    license='LGPL-3',
    url='https://github.com/dry-python/dependencies',
    author='Artem Malyshev',
    author_email='proofit404@gmail.com',
    packages=['dependencies'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',  # noqa: E501
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
)

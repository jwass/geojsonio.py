#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'geojsonio',
]

setup(
    name='geojsonio',
    version='0.0.1',
    description='geojsonio CLI - Python.',
    # long_description=readme + '\n\n' + history,
    author='Jacob Wasserman',
    author_email='jwasserman@gmail.com',
    packages=packages,
    package_data={'': ['LICENSE',]},
    package_dir={'geojsonio': 'geojsonio'},
    include_package_data=True,
    license='BSD',
    zip_safe=False,
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
    ),
    install_requires=[
        "github3.py>=0.7.0",
    ],
    entry_points={
      'console_scripts':
        ['geojsonio = geojsonio:main']
    }
)

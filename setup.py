from __future__ import unicode_literals

from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='geojsonio',
    version='0.0.3',
    description='geojsonio CLI - Python.',
    long_description=long_description,
    author='Jacob Wasserman',
    author_email='jwasserman@gmail.com',
    url='https://github.com/jwass/geojsonio.py',
    packages=find_packages(exclude=['ez_setup', 'tests']),
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
        "github3.py",
        "six",
    ],
    extras_require={
        'test': [
            "pytest",
            "mock",
        ]
    },
    entry_points={
      'console_scripts':
        ['geojsonio = geojsonio:main']
    }
)

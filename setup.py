from __future__ import unicode_literals

from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='geojsonio',
    version='0.0.2',
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
        "github3.py==0.9.3",
        "six==1.8.0",
    ],
    extras_require={
        'test': [
            "pytest==2.6.4",
            "mock==1.0.1",
        ]
    },
    entry_points={
      'console_scripts':
        ['geojsonio = geojsonio:main']
    }
)

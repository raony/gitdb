"""
https://github.com/raony/gitdb
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gitdb',

    version='0.1.0',

    description='Git client that uses git as a NoSQL database',
    long_description=long_description,

    url='https://github.com/raony/gitdb',

    author='raony',
    author_email='delvar@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='nosql git database',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'dulwich',
        'python-dateutil',
        'pyyaml',
    ],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['tox'],
    },

    setup_requires=['tox-setuptools'],
)

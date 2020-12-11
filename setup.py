#!/usr/bin/env python
# coding=utf-8

"""
python distribute file
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

from setuptools import setup, find_packages


def requirements_file_to_list(fn="requirements.txt"):
    """read a requirements file and create a list that can be used in setup.

    """
    with open(fn, 'r') as f:
        return [x.rstrip() for x in list(f) if x and not x.startswith('#')]


setup(
    name="threads",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requirements_file_to_list(),
    dependency_links=[],
    entry_points={
        # 'console_scripts': [
        #     'main = mypkg.main:main',
        # ]
    },
    package_data={
        'threads': ['logger.conf']
    },
    author="Augustin Peyrard",
    author_email="augustin.peyrard@gmail.com",
    description="Sandbox to play with some python threads",
    long_description=open('README.md').read(),
    license="MIT",
    url="https://github.com/a-peyrard/threads-sandbox",
)
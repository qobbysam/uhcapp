#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Admissions Pathway Application"""

import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_readme():
    """Return the README file contents. Supports text,rst, and markdown"""
    for name in ('README', 'README.rst', 'README.md'):
        if os.path.exists(name):
            return read_file(name)
    return ''

DESC = 'Application for montauk labs assesment'
setup(
    name="Uhc Application",
    version='1.0.0',
    url='',
    author='Samuel Abasah',
    author_email='kobabco@gmail.com',
    description=DESC,
    long_description=get_readme(),
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
    ],
)
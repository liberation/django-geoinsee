#!/usr/bin/env python
import os
from setuptools import setup
from setuptools import find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='django-geoinsee',
      version='0.1',
      description='Django French localities based on INSEE',
      long_description=read('README.rst'),
      author='Xavier Grangier',
      author_email='grangier@gmail.com',
      url='https://github.com/grangier/django-geoinsee',
      install_requires=['Django'],
      test_suite='geoinsee.tests.suite',
      packages=find_packages(exclude=['tests']),
)

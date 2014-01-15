#!/usr/bin/env python
import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='django-geoinsee',
      version='0.1',
      description='Django French localities based on INSEE',
      long_description=read('README.rst'),
      author='Xavier Grangier',
      author_email='grangier@gmail.com',
      url='https://https://github.com/grangier/django-geoinsee',
      packages=['geoinsee'],
     )

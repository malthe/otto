#!/usr/bin/env python # -- coding: utf-8 --

__version__ = '0.1'

import os
import re
import sys

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# information
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

# documentation
INTRO = open(os.path.join(here, 'docs', 'getting_started.rst')).read()
REFERENCE = open(os.path.join(here, 'docs', 'reference.rst')).read()
USERSGUIDE = open(os.path.join(here, 'docs', 'usersguide.rst')).read()
GUIDELINES = open(os.path.join(here, 'docs', 'guidelines.rst')).read()

long_description = "\n\n".join((
    README, INTRO, REFERENCE, USERSGUIDE, GUIDELINES, CHANGES))
long_description = long_description.replace('.. code-block:: python', '::')
long_description = re.sub(r':mod:`(\D+)`', '*\\1*', long_description)

version = sys.version_info[:3]

install_requires = []

setup(
    name="Otto",
    version=__version__,
    description="WSGI-compliant HTTP publisher.",
    long_description=long_description,
    classifiers=[
       "Development Status :: 3 - Alpha",
       "Intended Audience :: Developers",
       "Programming Language :: Python",
      ],
    keywords="wsgi publisher router",
    author="Malthe Borch",
    author_email="mborch@gmail.com",
    install_requires=install_requires,
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="otto.tests",
    tests_require = install_requires + ['manuel', 'WebOb'],
    )


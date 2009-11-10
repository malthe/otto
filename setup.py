#!/usr/bin/env python # -- coding: utf-8 --

__version__ = '1.0'

import os
import sys

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# information
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

ROLES = """\
.. role:: mod(emphasis)
.. role:: term(emphasis)
"""

long_description = "\n\n".join((
    ROLES, README, CHANGES))
long_description = long_description.replace('.. code-block:: python', '::')

version = sys.version_info[:3]

install_requires = ['WebOb']

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
    url="http://www.ottohttp.org",
    install_requires=install_requires,
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="otto.tests",
    tests_require = install_requires + ['manuel'],
    )


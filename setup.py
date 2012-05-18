#!/usr/bin/env python
import re
from setuptools import setup

VERSION_PATTERN = re.compile(r'VERSION\s*=\s*(.*)$', re.I)
VERSION = VERSION_PATTERN.search(open('paypal/__init__.py').read()) \
                         .groups()[0].strip().strip('\'"')

LONG_DESCRIPTION = \
"""An implementation of PayPal's API in Python. Currently features Direct
Payment (Guest), and PayPal Express checkouts."""

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

required = [
    'requests',
]

packages = [
    'paypal',
]

setup(name = 'paypal',
      version=VERSION,
      description='PayPal API implementation in Python.',
      long_description=LONG_DESCRIPTION,
      author= 'Pat Collins',
      author_email='pat@burned.com',
      maintainer='Gregory Taylor',
      maintainer_email='gtaylor@gc-taylor.com',
      install_requires=required,
      url='http://github.com/duointeractive/paypal-python/',
      download_url='http://pypi.python.org/pypi/paypal/',
      packages=packages,
      platforms=['Platform Independent'],
      license='Apache Software License',
      classifiers=CLASSIFIERS,
      keywords='paypal nvp',
 )

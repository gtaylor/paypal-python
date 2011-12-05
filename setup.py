#!/usr/bin/env python
import re

VERSION_PATTERN = re.compile(r'VERSION\s*=\s*(.*)$', re.I)
VERSION = VERSION_PATTERN.search(open('paypal/__init__.py').read()) \
                         .groups()[0].strip().strip('\'"')

from setuptools import setup

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

KEYWORDS = 'paypal nvp'

setup(name = 'paypal',
      version = VERSION,
      description = 'PayPal API implementation in Python.',
      long_description = LONG_DESCRIPTION,
      author = 'Pat Collins',
      author_email = 'pat@burned.com',
      maintainer = 'Gregory Taylor',
      maintainer_email = 'gtaylor@duointeractive.com',
      url = 'http://github.com/duointeractive/paypal-python/',
      download_url = 'http://pypi.python.org/pypi/paypal/',
      packages = ['paypal'],
      platforms = ['Platform Independent'],
      classifiers = CLASSIFIERS,
      keywords = KEYWORDS,
      use_2to3 = True
     )

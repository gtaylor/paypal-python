#!/usr/bin/env python

from distutils.core import setup
import paypal

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
                'Topic :: Software Development :: Libraries :: Python Modules' 
              ]

KEYWORDS = 'paypal nvp'

setup(name='paypal',
      version=paypal.VERSION,
      description='PayPal API implementation in Python.',
      long_description = LONG_DESCRIPTION,
      author='Pat Collins',
      author_email='pat@burned.com',
      maintainer='Gregory Taylor',
      maintainer_email='gtaylor@duointeractive.com',
      url='http://github.com/duointeractive/paypal-python/',
      download_url='http://pypi.python.org/pypi/paypal/',
      packages=['paypal'],
      platforms = ['Platform Independent'],
      classifiers = CLASSIFIERS,
      keywords = KEYWORDS,
     )

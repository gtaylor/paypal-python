#!/usr/bin/env python
"""
Execute this module to run all of the unit tests for paypal-python. If you
haven't already, read README and act accordingly or all of these tests
will fail.
"""
import os
import sys
# Prepare the path to use the included paypal module instead of the system
# one (if applicable).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import t_direct_payment
import t_express_checkout

# A list of the modules under the tests package that should be ran.
test_modules = [t_direct_payment, t_express_checkout]

# Fire off all of the tests.
for mod in test_modules:
    suite = unittest.TestLoader().loadTestsFromModule(mod)
    unittest.TextTestRunner(verbosity=1).run(suite)
"""
This module creates PayPalInterface objects for each of the unit test
modules to use. We create a new one for each unittest module to reduce any
chance of tainting tests by all of them using the same interface. IE: Values
getting modified.

See get_interface_obj() below, as well as the README in this tests directory.
"""
import sys
import os

# The unit tests import this module, so we'll do the path modification to use
# this paypal project instead of any potential globally installed ones.
project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not project_root_dir in sys.path:
    sys.path.insert(0, project_root_dir)

from paypal import PayPalInterface

try:
    import api_details
except ImportError:
    print """
    ERROR: No api_details.py file exists in your paypal/tests directory. Please 
    copy api_details_blank.py to api_details.py and modify the values to your 
    own API developer _test_ credentials.
    
    If you don't already have test credentials, please visit:
    
        https://developer.paypal.com
    
    """
    sys.exit(1)

def get_interface_obj():
    """
    Use this function to get a PayPalInterface object with your test API
    credentials (as specified in api_details.py). Create new interfaces for
    each unit test module to avoid potential variable pollution. 
    """
    return PayPalInterface(config=api_details.CONFIG)

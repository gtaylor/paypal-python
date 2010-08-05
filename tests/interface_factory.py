import sys
import os

project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not project_root_dir in sys.path:
    sys.path.insert(0, project_root_dir)

import paypal

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
    return paypal.PayPalInterface(config=api_details.CONFIG)

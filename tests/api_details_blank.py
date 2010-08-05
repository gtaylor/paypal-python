"""
This file contains your PayPal test account credentials. If you are just
getting started, you'll want to copy api_details_blank.py to api_details.py,
and substitute the placeholders below with your PayPal test account details.
"""
from paypal import PayPalConfig

# Enter your test account's API details here. You'll need the 3-token
# credentials, not the certificate stuff.
CONFIG = PayPalConfig(API_USERNAME = "xxx_xxx_apix.xxx.com",
                      API_PASSWORD = "xxxxxxxxxx",
                      API_SIGNATURE = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                      DEBUG_LEVEL=0)

"""
The following values may be found by visiting https://developer.paypal.com/,
clicking on the 'Test Accounts' navbar link in the sandbox, and looking at
the accounts listed there. You'll need a business and a personal account
created to run these tests.
"""
# The email address of your personal test account. This is typically the
# customer for these tests.
EMAIL_PERSONAL = 'custX_xxxxxxxxxx_per@xxxxxxxx.com'
# If you view the details of your personal account, you'll see credit card
# details. Enter the credit card number from there.
VISA_ACCOUNT_NO = 'xxxxxxxxxxxxxxxx'
# And the expiration date in the form of MMYYYY. Note that there are no slashes,
# and single-digit month numbers have a leading 0 (IE: 03 for march).
VISA_EXPIRATION = 'mmyyyy'
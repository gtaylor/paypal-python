PayPal-Python
=============

This package implements Paypal's Website Payments Pro NVP API in Python. 
This currently includes Direct Payments (Credit card payments without a PayPal 
Account) and PayPal Express Checkout (Payment via a PayPal account).

This module is best used in conjunction with the 
official PayPal `documentation`_. The stuff under
"Website Payments Pro and Express Checkout API Operations". in particular.

paypal-python does no real validation, doesn't hold hands, and is generally
only going to handle authentication, http-level stuff, and serializing
a list of keyword arguments passed to the API methods. You'll need to
read the official PayPal documentation for what key/values to pass.

.. _documentation: https://cms.paypal.com/us/cgi-bin/?cmd=_render-content&content_ID=developer/howto_api_reference

*NOTE: This module is not created by, endorsed by, or in any way affiliated
with PayPal.*

Requirements
------------

* Python 2.5, 2.6 or 2.7

Installation
------------
    
Through pip:
    pip install paypal
or easy_install:
    easy_install paypal
or download the source, un-tar/un-zip it, cd into paypal-python, and:
    python setup.py install

Quick Start
-----------

To run test suite, do from within the paypal-python directory:

    pip install nose
    nosetests tests/

The meat is in paypal.interface. The docs are in the docstrings and tests.

* Create a paypal.interface.PayPalInterface object
* Pass it configuration kwargs (See tests.interface_factory.get_interface_obj
  for a good example of how this works).
* That interface is how you access PayPal. Take a look at the currently
  implemented methods in paypal.interface.
  
Support/Help
------------

If you have any problems, questions, or ideas, feel free to post on our 
`issue tracker`_.

.. _issue tracker: http://github.com/duointeractive/paypal-python/issues)

Addendum A
----------

Instructions for setting up a Sandbox Website Payments Pro account. More 
detailed instructions can be found at [x.com](http://x.com) but this is what 
worked for me.

 1. Create Sandbox account. Don't use your live PayPal account email address.
 2. Login to Sandbox
 3. Test Accounts -> "Preconfigured" -- the manual process sucks.
 4. Make a "Seller" account
 5. Don't change "login email" at all -- it seems to truncate to 6 characters.
 6. I took the numeric password they gave as default and copy/pasted it into a 
    plain text document so I could use it later to make all my test account 
    passwords the same.
 7. I chose Visa as the credit card.
 8. Bank Account = "Yes" -- This is needed for a Verified account, which is 
    needed for Website Payments Pro.
 9. Put $1,000 of fake $$ into the account. At one point I tried $5,000 but 
    the test account I created wasn't Verified automatically? Not sure if the 
    two are related.
 10. No notes.
 11. "Create Account"
 12. When it takes you back to the "Test Accounts" screen, it should say 
     "Business" and "Verified"
 13. When you click on "API Credentials" you should see API credentials for the 
     corresponding test account you just created. I copy/pasted them into the 
     same text file used above.

The next step was the tricky part, at least for me. I was getting `10501` 
errors which means the billing agreement wasn't agreed to. Apparently you need 
to accept the fake billing agreement that comes along with the fake account you 
just created, which semi-conveniently has come packaged with an automatically 
created and verified fake bank account and business account "verified" status. 
Why couldn't the billing agreement be automatically "agreed to" as well?

Back on the "Test Accounts" page, choose the account you just created and click 
"Enter Sandbox Test Site." It should populate the fake email address, which 
should be `userna_XXXXXXXXXX_biz@domain.com`. Use the copy/pasted password from 
step #6 and paste it into the password field and login.

Now go under Merchant Services -> Website Payments Pro. In the right column 
there should be a link to "agree" to the billing agreement. Click this link and 
agree to the agreement. Now your API calls will work as expected.

LICENSE
-------

    Copyright 2009 Pat Collins <pat@burned.com>
    Copyright 2012 DUO Interactive, LLC <gtaylor@duointeractive.com>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

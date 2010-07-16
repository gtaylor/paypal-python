QUICKSTART
----------

To run test suite:

    python paypal/test.py

The meat is in `paypal.sdk.interface`. The docs are in the docstrings and tests.

- Create a paypal.sdk.interface.Interface object
- pass it configuration args
- that interface is how you access paypal.

Pat Collins' original was useful, but had the config info hardcoded into a 
Settings object.

So I refactored hid code into more of an OOP concept.

basically, you create a sdk.Interface() instace with the account details.  
that creates an internal config object of the PayPalConfig() class 
(was settings.py). this could be overriden by making a raw config object and 
explicitly setting it.

all of the original methods were migrated to the the Interface class -- and 
alphabetized -- as methods of that class.

the end result -- which i was going for -- is that i can now construct an 
interface with the account settings -- and not worry about editing config files 
and having to manually place this library in every project. It's also easier to 
lookup info.

-- Jonathan Vanasco ( jonathan@2xlp.com )

WHY?
----

The real value for me is having a working test suite with easy-to-understand 
and use methods on the APIs.

TODO
----

See TODO

Also, the following methods don't do much yet, because Express Checkout hasn't 
been implemented at all:

    address_verify
    do_authorization
    get_express_checkout_details
    
`set_express_checkout` technically works, but it needs 
`get_express_checkout_details` to do all of the work, and that method requires 
a PAYERID that you can only get if the user logs into PayPal.

ADDENDUM A
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

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

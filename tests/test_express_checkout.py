# coding=utf-8

import unittest
from . import interface_factory
from . import api_details

interface = interface_factory.get_interface_obj()

class TestExpressCheckout(unittest.TestCase):

    def setUp(self):
        self.returnurl = 'http://www.paypal.com'
        self.cancelurl = 'http://www.ebay.com'

    def test_sale(self):
        """
        Tests the first part of a sale. At this point, this is a partial unit
        test. The user has to login to PayPal and approve the transaction,
        which is not something we have tackled in the unit test yet. So we'll
        just test the set/get_express_checkout methods.
        
        A call to `SetExpressCheckoutDetails`.
        A call to `DoExpressCheckoutPayment`.
        A call to `GetExpressCheckoutDetails`.
        """
        setexp_response = interface.set_express_checkout(amt='10.00', 
            returnurl=self.returnurl, cancelurl=self.cancelurl, 
            paymentaction='Order', 
            email=api_details.EMAIL_PERSONAL)

        self.assertTrue(setexp_response)
        token = setexp_response.token

        getexp_response = interface.get_express_checkout_details(token=token)
        
        # Redirect your client to this URL for approval.
        redir_url = interface.generate_express_checkout_redirect_url(token)
        # Once they have approved your transaction at PayPal, they'll get
        # directed to the returnurl value you defined in set_express_checkout()
        # above. This view should then call do_express_checkout_payment() with
        # paymentaction = 'Sale'. This will finalize and bill. 

    def test_authorize_and_delayed_capture(self):
        """
        Tests a four-step checkout process involving the following flow::

            One or more calls to `SetExpressCheckout`.
            --- User goes to PayPal, logs in, and confirms shipping, taxes,
                and total amount. ---
            A call to `GetExpressCheckoutDetails`.
            A call to `DoExpressCheckoutPayment`.
            A call to `DoAuthorization`.
            A call to `DoCapture`.
        """
        pass

    def test_authorize_and_void(self):
        """
        Tests a four-step checkout process involving the following flow::

            One or more calls to `SetExpressCheckout`.
            --- User goes to PayPal, logs in, and confirms shipping, taxes,
                and total amount. ---
            A call to `GetExpressCheckoutDetails`.
            A call to `DoExpressCheckoutPayment`.
            A call to `DoAuthorization`.
            A call to `DoVoid`.
        """
        pass

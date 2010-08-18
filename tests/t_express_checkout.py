# coding=utf-8

import unittest
import interface_factory
import api_details

interface = interface_factory.get_interface_obj()

# TODO: implement the paypal account log-in as web-based? somehow implement with a bare-bones python web client so it's programmable?
class TestExpressCheckout(unittest.TestCase):
    def setUp(self):
        self.returnurl = 'http://www.paypal.com'
        self.cancelurl = 'http://www.ebay.com'

    def test_sale(self):
        """
        A call to `SetExpressCheckoutDetails`.
        A call to `DoExpressCheckoutPayment`.
        A call to `GetExpressCheckoutDetails`.
        """
        setexp_response = interface.set_express_checkout(paymentrequest_0_amt='10.00', 
            returnurl=self.returnurl, cancelurl=self.cancelurl, 
            paymentrequest_0_paymentaction='Order', 
            email=api_details.EMAIL_PERSONAL)
        self.assertTrue(setexp_response)
        token = setexp_response.token
        print setexp_response
        print "TOKEN", token
        print "REDIR URL: https://www.sandbox.paypal.com/webscr??cmd=_express-checkout&token=%s&AMT=%s&CURRENCYCODE=USD&RETURNURL=%s&CANCELURL=%s" % (
                                                        token, '10.00',
                                                        self.returnurl,
                                                        self.cancelurl)
        print "REDIR2  : %s" % interface.generate_express_checkout_redirect_url(token)
        getexp_response = interface.get_express_checkout_details(token)
        print getexp_response
        
        """
        This is where you'd redirect your user's browser to PayPal.
        
        https://www.sandbox.paypal.com/webscr
            ?cmd=_express-checkout&token=tokenValue
            &AMT=amount
            &CURRENCYCODE=currencyID
            &RETURNURL=return_url
            &CANCELURL=cancel_url
        """

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

if __name__ == '__main__':
    unittest.main()
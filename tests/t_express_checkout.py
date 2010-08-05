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
        pass

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
        setexp = interface.set_express_checkout(amt='10.00', returnurl=self.returnurl, \
                     cancelurl=self.cancelurl, paymentaction='Order', \
                     email=api_details.EMAIL_PERSONAL)
        self.assertTrue(setexp.success)
        # print(setexp)
        # getexp = get_express_checkout_details(token=setexp.token)
        # print(getexp)

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
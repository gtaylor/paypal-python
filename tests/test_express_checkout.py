# coding=utf-8

import unittest
import warnings

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
        setexp_response = interface.set_express_checkout(
            amt='10.00',
            returnurl=self.returnurl, cancelurl=self.cancelurl,
            paymentaction='Order',
            email=api_details.EMAIL_PERSONAL
        )

        self.assertTrue(setexp_response)
        token = setexp_response.token

        getexp_response = interface.get_express_checkout_details(token=token)

        # Redirect your client to this URL for approval.
        redirect_url = interface.generate_express_checkout_redirect_url(token)
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


class UrlGenerationTest(unittest.TestCase):

    def test_no_useraction(self):
        redirect_url = interface.generate_express_checkout_redirect_url(
            'token-abc')
        self.assertTrue(redirect_url.endswith(
            '/webscr?cmd=_express-checkout&token=token-abc'))

    def test_renders_useraction_commit(self):
        redirect_url = interface.generate_express_checkout_redirect_url(
            'token-abc', useraction='commit')
        redirect_path = ('/webscr?cmd=_express-checkout&token=token-abc'
                         '&useraction=commit')
        self.assertTrue(redirect_url.endswith(redirect_path))

    def test_renders_useraction_continue(self):
        redirect_url = interface.generate_express_checkout_redirect_url(
            'token-abc', useraction='continue')
        redirect_path = ('/webscr?cmd=_express-checkout&token=token-abc'
                         '&useraction=continue')
        self.assertTrue(redirect_url.endswith(redirect_path))

    def test_renders_any_useraction_with_warning(self):
        with warnings.catch_warnings(record=True) as warning_context:
            redirect_url = interface.generate_express_checkout_redirect_url(
                'token-abc', useraction='some_action')
            self.assertTrue(issubclass(warning_context[0].category,
                                       RuntimeWarning))
        redirect_path = ('/webscr?cmd=_express-checkout&token=token-abc'
                         '&useraction=some_action')
        self.assertTrue(redirect_url.endswith(redirect_path))

# coding=utf-8

import unittest
import warnings

from mock import patch, Mock

from . import interface_factory
from . import api_details
from paypal.exceptions import PayPalAPIResponseError, PayPalConfigError
from paypal.interface import PayPalInterface
from paypal.response import PayPalResponse

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


class CallParamsTest(unittest.TestCase):

    def setUp(self):
        self.configs_3token = {'API_USERNAME': 'test_username',
                               'API_PASSWORD': 'test_password',
                               'API_SIGNATURE': 'test_signature',
                               'API_AUTHENTICATION_MODE': '3TOKEN'}
        self.configs_certificate = {
            'API_USERNAME': 'test_username',
            'API_PASSWORD': 'test_password',
            'API_CERTIFICATE_FILENAME': 'test_cert_filename',
            'API_KEY_FILENAME': 'test_key_filename',
            'API_AUTHENTICATION_MODE': 'CERTIFICATE'}

    def test_returns_3token_call_params(self):
        interface = PayPalInterface(**self.configs_3token)
        call_kwargs = {'param_a': 'a1', 'param_b': 'b2'}
        call_params = interface._get_call_params('some_method', **call_kwargs)
        version = interface.config.API_VERSION
        expected_call_params = {'data': {'USER': 'test_username',
                                         'PWD': 'test_password',
                                         'SIGNATURE': 'test_signature',
                                         'PARAM_A': 'a1',
                                         'PARAM_B': 'b2',
                                         'METHOD': 'some_method',
                                         'VERSION': version},
                                'cert': None,
                                'url': interface.config.API_ENDPOINT,
                                'timeout': interface.config.HTTP_TIMEOUT,
                                'verify': interface.config.API_CA_CERTS}
        self.assertEqual(expected_call_params, call_params)

    def test_returns_unipay_call_params(self):
        interface = PayPalInterface(**self.configs_3token)
        interface.config.API_AUTHENTICATION_MODE = 'UNIPAY'
        interface.config.UNIPAY_SUBJECT = 'test_subject'
        call_kwargs = {'param_a': 'a1', 'param_b': 'b2'}
        call_params = interface._get_call_params('some_method', **call_kwargs)
        version = interface.config.API_VERSION
        expected_call_params = {'data': {'SUBJECT': 'test_subject',
                                         'PARAM_A': 'a1',
                                         'PARAM_B': 'b2',
                                         'METHOD': 'some_method',
                                         'VERSION': version},
                                'cert': None,
                                'url': interface.config.API_ENDPOINT,
                                'timeout': interface.config.HTTP_TIMEOUT,
                                'verify': interface.config.API_CA_CERTS}
        self.assertEqual(expected_call_params, call_params)

    def test_returns_certificate_call_params(self):
        interface = PayPalInterface(**self.configs_certificate)
        call_kwargs = {'param_a': 'a1', 'param_b': 'b2'}
        call_params = interface._get_call_params('some_method', **call_kwargs)
        version = interface.config.API_VERSION
        expected_call_params = {'data': {'USER': 'test_username',
                                         'PWD': 'test_password',
                                         'PARAM_A': 'a1',
                                         'PARAM_B': 'b2',
                                         'METHOD': 'some_method',
                                         'VERSION': version},
                                'cert': ('test_cert_filename',
                                         'test_key_filename'),
                                'url': interface.config.API_ENDPOINT,
                                'timeout': interface.config.HTTP_TIMEOUT,
                                'verify': interface.config.API_CA_CERTS}
        self.assertEqual(expected_call_params, call_params)

    def test_raises_error_for_single_none_config(self):
        interface = PayPalInterface(**self.configs_certificate)
        interface.config.API_USERNAME = None
        with self.assertRaisesRegexp(PayPalConfigError, 'USER'):
            interface._get_call_params('some_method', some_param=123)

    def test_raises_error_for_multiple_configs(self):
        interface = PayPalInterface(**self.configs_certificate)
        interface.config.API_USERNAME = None
        interface.config.API_PASSWORD = None
        with self.assertRaisesRegexp(PayPalConfigError, r'PWD.*USER'):
            interface._get_call_params('some_method', some_param=123)


class CallTest(unittest.TestCase):

    def test_posts_params(self):
        with patch('paypal.interface.requests.post') as post_mock:
            post_mock.return_value = Mock(text='ACK=SUCCESS')
            paypal_response = interface._call('some_method',
                                              param_a='a1',
                                              param_b='b2')
        expected_data = interface._get_call_params('some_method',
                                                   param_a='a1',
                                                   param_b='b2')
        post_mock.assert_called_once_with(**expected_data)
        self.assertIsInstance(paypal_response, PayPalResponse)
        self.assertTrue(paypal_response.success)

    def test_raises_configerror_on_error_response(self):
        with patch('paypal.interface.requests.post') as post_mock:
            post_mock.return_value = Mock(text='ACK=NO_SUCCESS')
            with self.assertRaises(PayPalAPIResponseError):
                interface._call('some_method', param='a')

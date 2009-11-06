# coding=utf-8

from sdk import *
import unittest

class TestDirectPayment(unittest.TestCase):
    def setUp(self):
        self.credit_card = {
            'amt': '10.00',
            'creditcardtype': 'Visa',
            'acct': '4812177017895760',
            'expdate': '012010',
            'cvv2': '962',
            'firstname': 'John',
            'lastname': 'Doe',
            'street': '1 Main St',
            'city': 'San Jose',
            'state': 'CA',
            'zip': '95131',
            'countrycode': 'US',
            'currencycode': 'USD',
        }

    # def test_address_verify(self):
    #     print(address_verify("patcol_1257523559_biz@gmail.com", "1 Main St", "95131"))

    def test_sale(self):
        sale = do_direct_payment('Sale', **self.credit_card)
        self.assertTrue(sale.success)

        details = get_transaction_details(sale.TRANSACTIONID)
        self.assertTrue(details.success)
        self.assertEqual(details.PAYMENTSTATUS.upper(), 'COMPLETED')
        self.assertEqual(details.REASONCODE.upper(), 'NONE')

    def test_abbreviated_sale(self):
        sale = do_direct_payment(**self.credit_card)
        self.assertTrue(sale.success)

        details = get_transaction_details(sale.TRANSACTIONID)
        self.assertTrue(details.success)
        self.assertEqual(details.PAYMENTSTATUS.upper(), 'COMPLETED')
        self.assertEqual(details.REASONCODE.upper(), 'NONE')

    def test_authorize_and_delayed_capture(self):
        # authorize payment
        auth = do_direct_payment('Authorization', **self.credit_card)
        self.assertTrue(auth.success)
        self.assertEqual(auth.AMT, self.credit_card['amt'])

        # capture payment
        captured = do_capture(auth.TRANSACTIONID, auth.AMT)
        self.assertTrue(captured.success)
        self.assertEqual(auth.TRANSACTIONID, captured.PARENTTRANSACTIONID)
        self.assertEqual(captured.PAYMENTSTATUS.upper(), 'COMPLETED')
        self.assertEqual(captured.REASONCODE.upper(), 'NONE')

    def test_authorize_and_void(self):
        # authorize payment
        auth = do_direct_payment('Authorization', **self.credit_card)
        self.assertTrue(auth.success)
        self.assertEqual(auth.AMT, self.credit_card['amt'])

        # void payment
        note = 'Voided the authorization.'
        void = do_void(auth.TRANSACTIONID, note)
        self.assertTrue(void.success)
        self.assertEqual(auth.TRANSACTIONID, void.AUTHORIZATIONID)

        details = get_transaction_details(auth.TRANSACTIONID)
        self.assertTrue(details.success)
        self.assertEqual(details.PAYMENTSTATUS.upper(), 'VOIDED')

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
        setexp = set_express_checkout(amt='10.00', returnurl=self.returnurl, \
                     cancelurl=self.cancelurl, paymentaction='Order', \
                     email='patcol_1257541103_per@gmail.com')
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

if __name__ == "__main__":
    cases = [
        TestDirectPayment,
        TestExpressCheckout,
    ]
    suite = unittest.TestSuite(map(unittest.TestLoader().loadTestsFromTestCase, cases))
    unittest.TextTestRunner(verbosity=2).run(suite)

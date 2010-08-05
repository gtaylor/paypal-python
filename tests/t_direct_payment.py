# coding=utf-8

import unittest
import interface_factory
import api_details

interface = interface_factory.get_interface_obj()

class TestDirectPayment(unittest.TestCase):
    def setUp(self):
        self.credit_card = {
            'amt': '10.00',
            'creditcardtype': 'Visa',
            'acct': api_details.VISA_ACCOUNT_NO,
            'expdate': api_details.VISA_EXPIRATION,
            'cvv2': '123',
            'firstname': 'John',
            'lastname': 'Doe',
            'street': '1313 Mockingbird Lane',
            'city': 'Beverly Hills',
            'state': 'CA',
            'zip': '90110',
            'countrycode': 'US',
            'currencycode': 'USD',
        }

    def test_sale(self):
        sale = interface.do_direct_payment('Sale', **self.credit_card)
        self.assertTrue(sale.success)

        details = interface.get_transaction_details(sale.TRANSACTIONID)
        self.assertTrue(details.success)
        self.assertEqual(details.PAYMENTSTATUS.upper(), 'COMPLETED')
        self.assertEqual(details.REASONCODE.upper(), 'NONE')

    def test_abbreviated_sale(self):
        sale = interface.do_direct_payment(**self.credit_card)
        self.assertTrue(sale.success)

        details = interface.get_transaction_details(sale.TRANSACTIONID)
        self.assertTrue(details.success)
        self.assertEqual(details.PAYMENTSTATUS.upper(), 'COMPLETED')
        self.assertEqual(details.REASONCODE.upper(), 'NONE')

    def test_authorize_and_delayed_capture(self):
        # authorize payment
        auth = interface.do_direct_payment('Authorization', **self.credit_card)
        self.assertTrue(auth.success)
        self.assertEqual(auth.AMT, self.credit_card['amt'])

        # capture payment
        captured = interface.do_capture(auth.TRANSACTIONID, auth.AMT)
        self.assertTrue(captured.success)
        self.assertEqual(auth.TRANSACTIONID, captured.PARENTTRANSACTIONID)
        self.assertEqual(captured.PAYMENTSTATUS.upper(), 'COMPLETED')
        self.assertEqual(captured.REASONCODE.upper(), 'NONE')

    def test_authorize_and_void(self):
        # authorize payment
        auth = interface.do_direct_payment('Authorization', **self.credit_card)
        self.assertTrue(auth.success)
        self.assertEqual(auth.AMT, self.credit_card['amt'])

        # void payment
        note = 'Voided the authorization.'
        void = interface.do_void(auth.TRANSACTIONID, note)
        self.assertTrue(void.success)
        self.assertEqual(auth.TRANSACTIONID, void.AUTHORIZATIONID)

        details = interface.get_transaction_details(auth.TRANSACTIONID)
        self.assertTrue(details.success)
        self.assertEqual(details.PAYMENTSTATUS.upper(), 'VOIDED')

if __name__ == '__main__':
    unittest.main()

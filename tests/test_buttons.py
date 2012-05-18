# coding=utf-8

import unittest
from . import interface_factory

interface = interface_factory.get_interface_obj()

class ButtonTests(unittest.TestCase):
    """
    These test the BM button API available in Payments Standard and up. This
    is the cheapest and most direct route towards accepting payments.
    """

    def test_create_button(self):
        """
        Tests the creation of a simple button. This particular one is not
        stored on the PayPal account.
        """
        button_params = {
            'BUTTONCODE': 'ENCRYPTED',
            'BUTTONTYPE': 'BUYNOW',
            'BUTTONSUBTYPE': 'SERVICES',
            'BUYNOWTEXT': 'PAYNOW',
            'LBUTTONVAR0': 'notify_url=http://test.com',
            'LBUTTONVAR1': 'amount=5.00',
            'LBUTTONVAR2': 'item_name=Testing',
            'LBUTTONVAR3': 'item_number=12345',
        }
        response = interface.bm_create_button(**button_params)
        self.assertEqual(response.ACK, 'Success')

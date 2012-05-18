# coding=utf-8

import unittest
from paypal import countries

class TestCountries(unittest.TestCase):

    def test_is_valid_country_abbrev(self):
        self.assertEqual(True, countries.is_valid_country_abbrev('US'))
        self.assertEqual(True, countries.is_valid_country_abbrev('us'))
        self.assertEqual(False, countries.is_valid_country_abbrev('us', 
                                                                 case_sensitive=True))
        
    def test_get_name_from_abbrev(self):
        us_fullval = 'United States of America'
        self.assertEqual(us_fullval, countries.get_name_from_abbrev('US'))
        self.assertEqual(us_fullval, countries.get_name_from_abbrev('us'))
        self.assertRaises(KeyError, countries.get_name_from_abbrev, 'us',
                         case_sensitive=True)

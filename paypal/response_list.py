# coding=utf-8
"""
PayPal response parsing of list syntax.
"""

import logging
import re

from paypal.response import PayPalResponse
from paypal.exceptions import PayPalAPIResponseError

logger = logging.getLogger('paypal.response')


class PayPalResponseList(PayPalResponse):
    """
    Subclass of PayPalResponse, parses L_style list items and
    stores them in a dictionary keyed by numeric index.

    NOTE: Don't access self.raw directly. Just do something like
    PayPalResponse.someattr, going through PayPalResponse.__getattr__().
    """
    skippable_error_codes = [
        'ERRORCODE', 'SHORTMESSAGE', 'LONGMESSAGE', 'SEVERITYCODE']

    def __init__(self, raw, config):
        self.raw = raw
        self.config = config

        l_regex = re.compile("L_([a-zA-Z]+)([0-9]{0,2})")
        # name-value pair list syntax documented at
        #  https://developer.paypal.com/docs/classic/api/NVPAPIOverview/#id084E30EC030
        # api returns max 100 items, so only two digits required

        self.list_items_dict = {}

        for key in self.raw.keys():
            match = l_regex.match(key)
            if match:
                index = match.group(2)
                d_key = match.group(1)

                if isinstance(self.raw[key], list) and len(self.raw[key]) == 1:
                    d_val = self.raw[key][0]
                else:
                    d_val = self.raw[key]
            
                # Skip error codes
                if d_key in self.skippable_error_codes:
                    continue

                if index in self.list_items_dict:
                    # Dict for index exists, update
                    self.list_items_dict[index][d_key] = d_val
                else:
                    # Create new dict
                    self.list_items_dict[index] = {d_key: d_val}

        # Log ResponseErrors from warning keys
        if self.raw['ACK'][0].upper() == self.config.ACK_SUCCESS_WITH_WARNING:
            self.errors = [PayPalAPIResponseError(self)]
            logger.error(self.errors)

    def items(self):
        # Convert dict like {'1':{},'2':{}, ...} to list
        return list(self.list_items_dict.values())
        
    def iteritems(self):
        for key in self.list_items_dict.keys():
            yield (key, self.list_items_dict[key])

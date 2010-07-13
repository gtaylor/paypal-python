# coding=utf-8

from settings import PayPalConfig

import socket
import urllib
import urllib2
from urlparse import urlsplit, urlunsplit

from response import Response
from exceptions import ApiError

import types

def _check_required( requires , **kwargs ):
    for req in requires :
        # paypal api is never mixed-case
        if req.lower() not in kwargs and req.upper() not in kwargs :
            raise ApiError('missing required : %s' % req )
    

def encode_utf8( **kwargs ):
    u2= kwargs
    for i in u2.keys():
        if isinstance( u2[i] , types.UnicodeType ):
            u2[i]= u2[i].encode('utf-8')
    return u2


class Interface(object):

    def __init__( self , **kwargs ):
        """core paypal interface"""
        
        self.config= PayPalConfig( **kwargs )
        
        
        
    def call( self , method , **kwargs ):
        """
        Wrapper method for executing all API commands over HTTP. This method is
        further used to implement wrapper methods listed here:
    
        https://www.x.com/docs/DOC-1374
    
        ``method`` must be a supported NVP method listed at the above address.
    
        ``kwargs`` will be a hash of
        """
        socket.setdefaulttimeout( self.config.HTTP_TIMEOUT )
    
        urlvalues = {
            'METHOD': method,
            'VERSION': self.config.API_VERSION
        }
    
        headers = {}
        if( self.config.API_AUTHENTICATION_MODE == "3TOKEN" ):
            # headers['X-PAYPAL-SECURITY-USERID'] = API_USERNAME
            # headers['X-PAYPAL-SECURITY-PASSWORD'] = API_PASSWORD
            # headers['X-PAYPAL-SECURITY-SIGNATURE'] = API_SIGNATURE
            urlvalues['USER'] = self.config.API_USERNAME
            urlvalues['PWD'] = self.config.API_PASSWORD
            urlvalues['SIGNATURE'] = self.config.API_SIGNATURE
        elif( self.config.API_AUTHENTICATION_MODE == "UNIPAY" ):
            # headers['X-PAYPAL-SECURITY-SUBJECT'] = SUBJECT
            urlvalues['SUBJECT'] = self.config.SUBJECT
        # headers['X-PAYPAL-REQUEST-DATA-FORMAT'] = 'NV'
        # headers['X-PAYPAL-RESPONSE-DATA-FORMAT'] = 'NV'
        # print(headers)
        for k,v in kwargs.iteritems():
            urlvalues[k.upper()] = v
            
        if self.config.DEBUG_LEVEL >= 2 :
            k= urlvalues.keys()
            k.sort()
            for i in k:
               print " %-20s : %s" % ( i , urlvalues[i] )

        u2= encode_utf8( **urlvalues )

        data = urllib.urlencode(u2)
        req = urllib2.Request( self.config.API_ENDPOINT , data , headers )
        response = Response( urllib2.urlopen(req).read() , self.config )

        if self.config.DEBUG_LEVEL >= 1 :
            print self.config.API_ENDPOINT
    
        if not response.success:
            if self.config.DEBUG_LEVEL >= 1 :
                print response
            raise ApiError(response)

        return response



    def address_verify( self, email , street , zip ):
        """Shortcut for the AddressVerify method.
    
        ``email``::
            Email address of a PayPal member to verify.
            Maximum string length: 255 single-byte characters
            Input mask: ?@?.??
        ``street``::
            First line of the billing or shipping postal address to verify.
    
            To pass verification, the value of Street must match the first three
            single-byte characters of a postal address on file for the PayPal member.
    
            Maximum string length: 35 single-byte characters.
            Alphanumeric plus - , . ‘ # \
            Whitespace and case of input value are ignored.
        ``zip``::
            Postal code to verify.
    
            To pass verification, the value of Zip mustmatch the first five
            single-byte characters of the postal code ofthe verified postal
            address for the verified PayPal member.
    
            Maximumstring length: 16 single-byte characters.
            Whitespace and case of input value are ignored.
        """
        args= locals()
        del args['self']
        return self.call('AddressVerify', **args)



    def do_authorization( self, transactionid , amt ):
        """Shortcut for the DoAuthorization method.
    
        Use the TRANSACTIONID from DoExpressCheckoutPayment for the
        ``transactionid``. The latest version of the API does not support the
        creation of an Order from `DoDirectPayment`.
    
        The `amt` should be the same as passed to `DoExpressCheckoutPayment`.
    
        Flow for a payment involving a `DoAuthorization` call::
    
             1. One or many calls to `SetExpressCheckout` with pertinent order
                details, returns `TOKEN`
             1. `DoExpressCheckoutPayment` with `TOKEN`, `PAYMENTACTION` set to
                Order, `AMT` set to the amount of the transaction, returns
                `TRANSACTIONID`
             1. `DoAuthorization` with `TRANSACTIONID` and `AMT` set to the
                amount of the transaction.
             1. `DoCapture` with the `AUTHORIZATIONID` (the `TRANSACTIONID`
                returned by `DoAuthorization`)
    
        """
        args= locals()
        del args['self']
        return self.call('DoAuthorization', **args)



    def do_capture( self , authorizationid , amt , completetype='Complete' , **kwargs ):
        """Shortcut for the DoCapture method.
    
        Use the TRANSACTIONID from DoAuthorization, DoDirectPayment or
        DoExpressCheckoutPayment for the ``authorizationid``.
    
        The `amt` should be the same as the authorized transaction.
        """
        kwargs.update(locals())
        del kwargs['self']
        return self.call('DoCapture', **kwargs)



    def do_direct_payment( self , paymentaction="Sale" , **kwargs):
        """Shortcut for the DoDirectPayment method.
    
        ``paymentaction`` could be 'Authorization' or 'Sale'
    
        To issue a Sale immediately::
    
            charge = {
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
            direct_payment("Sale", **charge)
    
        Or, since "Sale" is the default:
    
            direct_payment(**charge)
    
        To issue an Authorization, simply pass "Authorization" instead of "Sale".
    
        You may also explicitly set ``paymentaction`` as a keyword argument:
    
            ...
            direct_payment(paymentaction="Sale", **charge)
        """
        kwargs.update(locals())
        del kwargs['self']
        return self.call('DoDirectPayment', **kwargs)



    def do_void( self , authorizationid , note='' ):
        """Shortcut for the DoVoid method.
    
        Use the TRANSACTIONID from DoAuthorization, DoDirectPayment or
        DoExpressCheckoutPayment for the ``authorizationid``.
        """
        args= locals()
        del args['self']
        return self.call('DoVoid', **args)
    


    def get_express_checkout_details( self , token):
        """Shortcut for the GetExpressCheckoutDetails method.
        """
        return self.call('GetExpressCheckoutDetails', token=token)
        


    def get_transaction_details( self , transactionid ):
        """Shortcut for the GetTransactionDetails method.
    
        Use the TRANSACTIONID from DoAuthorization, DoDirectPayment or
        DoExpressCheckoutPayment for the ``transactionid``.
        """
        args= locals()
        del args['self']
        return self.call('GetTransactionDetails', **args)



    def set_express_checkout_legacy( self , amt , returnurl , cancelurl , token='' , **kwargs ):
        """Shortcut for the SetExpressCheckout method.
        """
        kwargs.update(locals())
        del kwargs['self']
        return self.call('SetExpressCheckout', **kwargs)


    def set_express_checkout( self , token='' , **kwargs ):
        """Shortcut for the SetExpressCheckout method.
            JV did not like the original method. found it limiting.
        """
        kwargs.update(locals())
        _check_required( ('amt',) , **kwargs )
        del kwargs['self']
        return self.call('SetExpressCheckout', **kwargs)


    def do_express_checkout_payment( self , token , **kwargs ):
        """Shortcut for the DoExpressCheckoutPayment method.
        
            Required
                *METHOD
                *TOKEN
                PAYMENTACTION
                PAYERID
                AMT
                
            Optional
                RETURNFMFDETAILS
                GIFTMESSAGE
                GIFTRECEIPTENABLE
                GIFTWRAPNAME
                GIFTWRAPAMOUNT
                BUYERMARKETINGEMAIL
                SURVEYQUESTION
                SURVEYCHOICESELECTED
                CURRENCYCODE
                ITEMAMT
                SHIPPINGAMT
                INSURANCEAMT
                HANDLINGAMT
                TAXAMT

            Optional + USEFUL
                INVNUM - invoice number
                
        """
        kwargs.update(locals())
        _check_required( ('paymentaction','payerid') , **kwargs )
        del kwargs['self']
        return self.call('DoExpressCheckoutPayment', **kwargs)
        
        
    def generate_express_checkout_redirect_url( self, token ):
        """submit token, get redirect url for client"""
        url= "%s?cmd=_express-checkout&token=%s" % ( self.config.PAYPAL_URL_BASE , token )
        return url
        
    
    def generate_cart_upload_redirect_url( self,  **kwargs ):
        """https://www.sandbox.paypal.com/webscr 
            ?cmd=_cart
            &upload=1
        """
        _check_required( ('business','item_name_1','amount_1','quantity_1') , **kwargs )
        url= "%s?cmd=_cart&upload=1" % ( self.config.PAYPAL_URL_BASE  )
        additional= encode_utf8( **kwargs )
        additional= urllib.urlencode(additional)
        url= url + "&" + additional
        return url

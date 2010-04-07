# coding=utf-8

from exceptions import *

class PayPalConfig(object):

    _valid_= {
        'API_ENVIRONMENT' : ['sandbox','production'],
        'API_AUTHENTICATION_MODE' : ['3TOKEN','CERTIFICATE'],
    }

    _API_ENDPOINTS= {
        '3TOKEN': {
            'sandbox' : 'https://api-3t.sandbox.paypal.com/nvp',
            'production' : 'https://api-3t.paypal.com/nvp',
        }
    }

    _PAYPAL_URL_BASE= {
        'sandbox' : 'https://www.sandbox.paypal.com/webscr',
        'production' : 'https://www.paypal.com/webscr',
    }

    API_VERSION = "60.0"

    # defaults
    API_ENVIRONMENT= 'sandbox'
    API_AUTHENTICATION_MODE= '3TOKEN'

    # 3TOKEN credentials
    API_USERNAME = None
    API_PASSWORD = None
    API_SIGNATURE = None

    API_ENDPOINT= None
    PAYPAL_URL_BASE= None
    
    # UNIPAY credentials
    UNIPAY_SUBJECT = None
    
    ACK_SUCCESS = "SUCCESS"
    ACK_SUCCESS_WITH_WARNING = "SUCCESSWITHWARNING"
    
    DEBUG_LEVEL= 0

    # in seconds
    HTTP_TIMEOUT = 15
    
    RESPONSE_KEYERROR= "AttributeError"
    
    KEY_ERROR= True
    
    

    def __init__(self, **kwargs):

        print kwargs

        if 'API_ENVIRONMENT' not in kwargs:
            kwargs['API_ENVIRONMENT']= self.API_ENVIRONMENT
        if kwargs['API_ENVIRONMENT'] not in self._valid_['API_ENVIRONMENT']:
            raise ApiError('Invalid API_ENVIRONMENT')
        self.API_ENVIRONMENT= kwargs['API_ENVIRONMENT']

        if 'API_AUTHENTICATION_MODE' not in kwargs:
            kwargs['API_AUTHENTICATION_MODE']= self.API_AUTHENTICATION_MODE
        if kwargs['API_AUTHENTICATION_MODE'] not in self._valid_['API_AUTHENTICATION_MODE']:
            raise ApiError("Not a supported auth mode. Use one of: %s" % \
                           ", ".join(self._valid_['API_AUTHENTICATION_MODE']))
        
        # set the endpoints
        self.API_ENDPOINT= self._API_ENDPOINTS[self.API_AUTHENTICATION_MODE][self.API_ENVIRONMENT]
        self.PAYPAL_URL_BASE= self._PAYPAL_URL_BASE[self.API_ENVIRONMENT]        
        
        # set the 3TOKEN required fields
        if self.API_AUTHENTICATION_MODE == '3TOKEN':
            for arg in ('API_USERNAME','API_PASSWORD','API_SIGNATURE'):
                if arg not in kwargs:
                    raise ApiError('Missing in PayPalConfig: %s ' % arg )
                setattr( self , arg , kwargs[arg] )
                
        for arg in ( 'HTTP_TIMEOUT' , 'DEBUG_LEVEL' , 'RESPONSE_KEYERROR' ):
            if arg in kwargs:
                setattr( self , arg , kwargs[arg] )
        

    



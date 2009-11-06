# coding=utf-8

API_ENDPOINT = "https://api-3t.sandbox.paypal.com/nvp"

# 3TOKEN or UNIPAY
API_AUTHENTICATION_MODE = "3TOKEN"

# 3TOKEN credentials
API_USERNAME = "patcol_1257523559_biz_api1.gmail.com"
API_PASSWORD = "1257523570"
API_SIGNATURE = "AFcWxV21C7fd0v3bYYYRCpSSRl31AZEdoFKAMvYbAXdM9nKSDcaUlXDp"

# UNIPAY credential
# SUBJECT = "patcol_1257523559_biz@gmail.com"

# TODO: implement use of API via http proxy
USE_PROXY = False
PROXY_HOST = "127.0.0.1"
PROXY_PORT = "808"

# in seconds
HTTP_TIMEOUT = 15

PAYPAL_URL = "https://www.sandbox.paypal.com/webscr?cmd=_express-checkout&token="

VERSION = "60.0"

ACK_SUCCESS = "SUCCESS"
ACK_SUCCESS_WITH_WARNING = "SUCCESSWITHWARNING"


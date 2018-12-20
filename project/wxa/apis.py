import json
import time
import random
import string
import hashlib
import logging
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
from django.core.cache import cache
from django.conf import settings
import xmltodict

def dicttoxml(dictdata, result=''):
    """ transfer dict object to xml string """
    for key, value in dictdata.items():
        if type(value).__name__ == 'dict':
            result += '<%s>%s</%s>' % (key, dicttoxml(value, result), key)
        else:
            result += '<%s>%s</%s>' % (key, value, key)
    return result



logger = logging.getLogger(__name__)

class WxaApi():

    appid = 'wx5ce51f801b09fb8b'
    secret = '734e3979b8cc50e54fb578a3413eaae7'
    mchid = '1514255601'
    key = '79DF20197DB57B38B0CD5581AEA6CF3A'

    def _getData(self, url, data=''):
        "Get data from url."
        data = data.encode('UTF-8')
        response = urlopen(url, data)
        result = response.read().decode('utf-8')
        response.close()
        return json.loads(result)

    def _getNonce(self, length=32):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def _sign(self, data):
        data = urlencode(sorted(data.items()))
        data = unquote(data)
        data += '&key=' + self.key
        data = str.encode(data)
        sign = hashlib.md5(data).hexdigest().upper()
        return sign


    def _getToken(self):
        access_token = cache.get('wx_access_token')
        if access_token:
            return access_token
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.appid, self.secret)
        data = self._getData(url)
        cache.set(
            'wx_access_token',
            data['access_token'],
            int(data['expires_in'])
        )
        return data['access_token']


    def getOpenid(self, code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code'% (self.appid, self.secret, code)
        result = self._getData(url)
        try:
            return (result['openid'], None)
        except:
            return (None, result['errmsg'])


    def getQrcode(self, qrcodestr):
        """ create qrcode """
        access_token = self._getToken()
        url = 'https://api.weixin.qq.com/cgi-bin/wxaapp/createwxaqrcode?access_token=%s' % access_token
        data = {'path': '/pages/index/index?p=%s' % qrcodestr}
        data = json.dumps(data).encode('utf-8')
        result = urlopen(url, data)
        qrcode = result.read()
        result.close()

        f_name = hashlib.md5(str.encode(qrcodestr)).hexdigest()
        f_full_name = '%s/%s/%s.jpg' % (
            settings.MEDIA_ROOT,
            'wxa/qrcode',
            f_name
        )
        f_url = '%s%s/%s.jpg' % (
            settings.MEDIA_URL,
            'wxa/qrcode',
            f_name
        )
        f = open(f_full_name, 'wb')
        f.write(qrcode)
        f.close()
        return f_url


    def _getPrepayId(self, data):
        """ get wechat uniferpay id"""
        data.update({
            'trade_type': 'JSAPI',
            'appid': self.appid,
            'mch_id': self.mchid,
            'nonce_str': self._getNonce()
        })
        data['sign'] = self._sign(data)
        data = {'xml':data}

        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        data = dicttoxml(data)
        response = urlopen(url, str.encode(data))
        result = response.read()
        response.close()
        result = dict(xmltodict.parse(result))

        if result['xml']['return_code'] == 'SUCCESS':
            return result['xml']['prepay_id']
        return False


    def getPayData(self, data):
        """ get wxa pay data dict """
        prepay_id = self._getPrepayId(data)
        if not prepay_id:
            return False
        newdata = {
            'appId': self.appid,
            'timeStamp': str(int(time.time())),
            'nonceStr': self._getNonce(),
            'package': 'prepay_id='+prepay_id,
            'signType': 'MD5'
        }
        sign = self._sign(newdata)
        newdata.update({'paySign':sign})
        return newdata

    def sendMessage(self, data):
        """ send template message """
        token = self._getToken()
        url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=' + token
        data = json.dumps(data).encode('utf-8')
        response = urlopen(url, data)
        result = response.read().decode('utf-8')
        response.close()
        return json.loads(result)

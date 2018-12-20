import time
from django.test import TestCase
from .models import Wxa
from .apis import WxaApi

class WxaTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_wxa(self):
        """Create wxa object test"""
        obj = Wxa.objects.create_wxa(str(time.time()))
        self.assertIs(obj, True)

    def test_make_qrcode(self):
        """test make qrcode"""
        api = WxaApi()
        result = api.getQrcode()
        self.assertIs(result, True)

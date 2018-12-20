from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class WxaConfig(AppConfig):
    name = 'wxa'
    verbose_name = _('wxa')

    def ready(self):
        import wxa.receivers

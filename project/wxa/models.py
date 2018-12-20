from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .signals import *

class WxaManager(models.Manager):
    def create_wxa(self, openid, p=None):
        """ create wxa user """
        user = User.objects.create_user('None', '', '')
        user.username = user.id
        user.save()
        Token.objects.get_or_create(user=user)
        register_success.send(sender=self.__class__, user=user, p=p)
        obj = self.create(user=user, openid=openid)
        return obj


class Wxa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
            verbose_name=_('user'))
    nickname = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    openid = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = WxaManager()

    def __str__(self):
        if not self.nickname:
            return str(self.user)
        return self.nickname

    class Meta:
        ordering = ['-created']
        verbose_name = _('wxa user')
        verbose_name_plural = _('wxa user')

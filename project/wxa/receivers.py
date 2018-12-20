from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .signals import *

#@receiver(register_success)
#def create_auth_token(sender, **kwargs):
#    user = kwargs['user']
#    return Token.objects.create(user=user)


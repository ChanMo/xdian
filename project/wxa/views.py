import logging
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *
from .apis import *

logger = logging.getLogger(__name__)

@api_view(['POST'])
def login(request):
    code = request.data['code']
    p = request.data['p']
    api = WxaApi()
    openid, message = api.getOpenid(code)
    if not openid:
        return Response({'error':'get openid error: ' + message}
                ,status=status.HTTP_400_BAD_REQUEST)
    try:
        obj = Wxa.objects.get(openid=openid)
    except Wxa.DoesNotExist:
        obj = Wxa.objects.create_wxa(openid=openid, p=p)
    return Response({'token':obj.user.auth_token.key,'id':obj.user.id})


@api_view(['GET'])
def me(request):
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    key = token.key
    if not created:
        key = token.generate_key()
        Token.objects.filter(user=user).update(key=key)
    return Response({'token':key,'id':user.id})


class SyncView(UpdateAPIView):
    model = Wxa
    serializer_class = WxaSerializer

    def get_object(self):
        return Wxa.objects.get(user=self.request.user)

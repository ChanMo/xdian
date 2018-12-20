from django.urls import path
from .views import *

urlpatterns = [
    path('me/', me),
    path('login/', login),
    path('sync/', SyncView.as_view())
]

from django.urls import path,include
from django.conf.urls import url

from .consumers import IndexConsumer

ws_urlpatterns = [
    path('ws',IndexConsumer.as_asgi()),
]
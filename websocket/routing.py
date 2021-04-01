from django.urls import path
from django.conf.urls import url

from .consumers import IndexConsumer

ws_urlpatterns = [
    path('ws/status/',IndexConsumer.as_asgi())
]
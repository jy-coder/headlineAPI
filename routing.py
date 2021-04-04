
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, include
from websocket.routing import ws_urlpatterns

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application =ProtocolTypeRouter({
    'websocket': URLRouter([
        path('', URLRouter(
        ws_urlpatterns
    ))
    ])
})

from django.urls import re_path 
  
from . import consumers 
  
websocket_urlpatterns = [ 
    re_path(r'^ws/count/$', consumers.Counter.as_asgi()), 
] 


from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from drinks.consumers import Counter

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/count/', Counter.as_asgi()),
    ])
})
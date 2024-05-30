"""
ASGI config for drinks project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

import django 
from channels.auth import AuthMiddlewareStack 
from channels.routing import ProtocolTypeRouter, URLRouter 
from django.core.asgi import get_asgi_application
import drinks.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drinks.settings')
django.setup()

# application = get_asgi_application()

application = ProtocolTypeRouter({ 
  "http": get_asgi_application(), 
  "websocket": AuthMiddlewareStack( 
        URLRouter( 
            drinks.routing.websocket_urlpatterns 
        ) 
    ), 
})
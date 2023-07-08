"""
ASGI config for forestreeApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forestreeApp.settings')

django_asgi_app = get_asgi_application()



from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
import chat.routing
from .middleware import QueryAuthMiddleware


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
            QueryAuthMiddleware(URLRouter(chat.routing.websocket_urlpatterns))
        ),
})
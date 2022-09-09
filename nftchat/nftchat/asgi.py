import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nftchat.settings')

application = ProtocolTypeRouter({ 
    "http" : get_asgi_application(),
     "websocket": AuthMiddlewareStack( # 추가
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

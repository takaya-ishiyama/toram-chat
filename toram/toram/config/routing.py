from django.urls import include, path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from django.urls import path
# from chatapp.consumers import *

# websocket_urlpatterns = [
#     path('<str:room_name>', ChatConsumer),
# ]
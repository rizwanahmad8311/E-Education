from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/ac/<str:groupname>/',consumers.MyAsyncConsumer.as_asgi())
]
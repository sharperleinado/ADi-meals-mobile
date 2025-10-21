from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path("ws/authentication/otp", consumers.CountdownConsumer.as_asgi()),
]
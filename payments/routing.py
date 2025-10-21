from django.urls import path,re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r"ws/payments/all_transactions/(?P<order_id>\d+)/$", consumers.OrderUpdateConsumer.as_asgi()),
]

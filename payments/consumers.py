import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class OrderUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
        self.group_name = f"order_{self.order_id}"
        #print(f"👥 Client joined group {self.group_name}")
        #print(self.group_name)
        #print(self.order_id)

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    #Receive message from group
    async def order_update(self, event):
        await self.send(text_data=json.dumps({
            "order_id": event["order_id"],
            "food_value": event["food_value"],
        }))

        


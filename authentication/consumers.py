import asyncio
from datetime import datetime,timedelta
from channels.generic.websocket import AsyncWebsocketConsumer
import json



class CountdownConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # load from session scope (via AuthMiddlewareStack)
        valid_date_str = self.scope["session"].get("otp_valid_date")
        if valid_date_str:
            self.valid_date = datetime.fromisoformat(valid_date_str)

            while True:
                if not self.valid_date:
                    break
                time_diff = self.valid_date - datetime.now()

                if datetime.now() >= self.valid_date:
                    await self.send(json.dumps({"message": "Countdown reached ZERO!"}))
                    break

                hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)

                await self.send(json.dumps({
                    "hours": hours,
                    "minutes": minutes,
                    "seconds": seconds,
                }))

                await asyncio.sleep(1)

        
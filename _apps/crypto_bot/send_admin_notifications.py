import asyncio
import random

class SendNotifications:
    def __init__(self, main_class):
        self.main_class = main_class

    async def send_notifications(self, user_ids:list, text:str) -> bool:
        try:
            for id in user_ids:
                await self.main_class.bot.send_message(id, text, disable_notification=True)
                await asyncio.sleep(random.randrange(1, 3))
            return True
        except Exception as ex:
            print("SendNotifications", ex)
            return False
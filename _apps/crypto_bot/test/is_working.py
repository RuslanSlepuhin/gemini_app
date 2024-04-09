import asyncio
from datetime import datetime
from _apps.crypto_bot.variables import admin_id

text_text = "fsdafaaaaaaaaffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff dssssssssssssssssssssssssssssssss" \
            " ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaa" \
            "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffsssssssssssssss ss" \
            "sdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddfffffffffffffffffffffsssssssssss dddddddd"

class IsWorking:
    def __init__(self, main_class):
        self.main_class = main_class
        self.msg = None
        self.text = ""

    async def send_message_schedule(self, chat_id=admin_id, frequency=60*30, message="I'm at work"):
        while True:
            if not self.msg:
                self.text = message + "\n" +  datetime.now().strftime("%d-%m_%y %H:%M")
                self.msg = await self.main_class.bot.send_message(chat_id, self.text, disable_notification=True)
                await asyncio.sleep(frequency)
            elif len(self.text + datetime.now().strftime("%d-%m_%y %H:%M")) > 4096:
                    self.msg = None
            else:
                self.text += f"\n{datetime.now().strftime('%d-%m_%y %H:%M')}"
                await self.msg.edit_text(self.text)
                await asyncio.sleep(frequency)


import configparser
import time

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from _apps.real_estate_bot import variables

class TelegramBot:

    def __init__(self):
        self.client = None

    async def connect_client(self):
        config = configparser.ConfigParser()
        config.read(variables.project_base_path + "settings/config.ini")
        api_id = config['Telegram']['api_id']
        api_hash = config['Telegram']['api_hash']
        session = config['Telegram']['session']
        client = TelegramClient(session, int(api_id), api_hash)
        await client.connect()
        return client

    async def get_messages(self, channel_names:list, limit_msg:int=0):
        all_messages = []
        self.client = await self.connect_client()
        for channel in channel_names:
            all_messages.extend(await self.get_messages_from_channels(channel, limit_msg))
            pass
        await self.client.disconnect()
        return all_messages


    async def get_messages_from_channels(self, channel, limit_msg:int=0):

        all_messages = []  # список всех сообщений
        self.count_message_in_one_channel = 1
        offset_msg = 0  # номер записи, с которой начинается считывание
        # limit_msg = 1   # максимальное число записей, передаваемых за один раз
        total_messages = 0
        total_count_limit = limit_msg  # значение 0 = все сообщения
        history = None

        while True:
            try:
                history = await self.client(GetHistoryRequest(
                    peer=channel,
                    offset_id=offset_msg,
                    offset_date=None, add_offset=0,
                    limit=limit_msg, max_id=0, min_id=0,
                    hash=0))
            except Exception as e:
                try:
                    history = await self.get_messages_from_group(channel, limit_msg)
                except Exception as ex:
                    print("Exception GET_CONTENT VIEW.PY REAL_ESTATE_BOT:", ex)
                    time.sleep(2)

            # if not history.messages:
            if not history:
                print(f'Not history for channel {channel}')
                break

            messages = history.messages
            for message in messages:
                if message.message:  # если сообщение пустое, например "Александр теперь в группе"
                    all_messages.append(message.to_dict())

            try:
                offset_msg = messages[len(messages) - 1].id
            except Exception as e:
                print('192 - offset_msg = messages[len(messages) - 1].id\n', e)
                break
            total_messages = len(all_messages)
            if (total_count_limit != 0 and total_messages >= total_count_limit) or not messages:
                break
        filtered_messages = await self.messages_filter(all_messages)
        return filtered_messages

    async def get_messages_from_group(self, group_name:str|int, limit:int=0):
            messages = await self.client.get_messages(group_name, limit)
            for message in messages:
                print(message.sender_id, message.text)

    async def messages_filter(self, messages):
        filtered_messages = []
        for message in messages:
            for key_word in variables.pattern:
                if key_word in message['message']:
                    filtered_messages.append(message['message'])
        return filtered_messages
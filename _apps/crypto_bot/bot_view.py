import asyncio
from typing import Any
from _apps.crypto_bot.db.db_methods import create_table_users, insert_db
from aiogram import types, Router, F
from aiogram.dispatcher import router
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder

from _apps.crypto_bot import variables

class CryptoBotMethods:
    def __init__(self, Crypto_Bot):
        self.Crypto_Bot = Crypto_Bot
        self.min_per_hour = 2

    async def is_subscribed(self) -> bool:
        try:
            chat_member = await self.Crypto_Bot.bot.get_chat_member(
                chat_id=variables.crypto_channel_id,
                user_id=self.Crypto_Bot.message.chat.id
            )
            if chat_member.status in ["member", "creator"]:
                return True
            else:
                return False
        except:
            return False

    async def take_dialog(self):
        await self.Crypto_Bot.bot.send_message(self.Crypto_Bot.message.chat.id, 'TEST')
        for step in range(1, len(variables.media_way)+1):
            if not await self.is_subscribed():
                content = variables.media_way[step]
                await self.public_content(content)
            else:
                await self.Crypto_Bot.bot.send_message(self.Crypto_Bot.message.chat.id, variables.you_are_subscribed)
                print('break')
                break

    async def public_content(self, content):
        markup = None
        for key in content:
            match key:
                case "video_notes":
                    for note in content[key]:
                        file = FSInputFile(note)
                        await self.Crypto_Bot.bot.send_video_note(self.Crypto_Bot.message.chat.id, video_note=file)
                case "videos":
                    if len(content[key]) > 1:
                        media_group = []
                        for video_path in content[key]:
                            media_group.append(types.InputMediaVideo(media=FSInputFile(video_path)))
                        await self.Crypto_Bot.bot.send_media_group(self.Crypto_Bot.message.chat.id, media=media_group)
                    elif content[key]:
                        file = FSInputFile(content[key][0])
                        await self.Crypto_Bot.bot.send_video(self.Crypto_Bot.message.chat.id, video=file)
                case "pictures":
                    if len(content[key]) > 1:
                        media_group = []
                        for photo_path in content[key]:
                            media_group.append(types.InputMediaPhoto(media=FSInputFile(photo_path)))
                        await self.Crypto_Bot.bot.send_media_group(self.Crypto_Bot.message.chat.id, media=media_group)
                    elif content[key]:
                        file = FSInputFile(content[key][0])
                        await self.Crypto_Bot.bot.send_photo(self.Crypto_Bot.message.chat.id, photo=file)
                case "button":
                    markup = await self.get_markdown(content['button']['text'], content['button']['url'])
                case "texts":
                    for text in content[key]:
                        if markup and content[key].index(text) == len(content[key])-1:
                            await self.Crypto_Bot.bot.send_message(self.Crypto_Bot.message.chat.id, text, reply_markup=markup, disable_web_page_preview=True)
                        else:
                            await self.Crypto_Bot.bot.send_message(self.Crypto_Bot.message.chat.id, text, disable_web_page_preview=True)
                case 'timer':
                    if content['timer']:
                        print('sleep content[timer]', content['timer'])
                        await asyncio.sleep(content['timer'] * self.min_per_hour)

        # if content.get('timer') and content['timer']:
        #     print('sleep content[timer]', content['timer'])
        #     await asyncio.sleep(content['timer']*self.min_per_hour)


    async def get_markdown(self, button_text, callback_url):
        markup = InlineKeyboardBuilder()
        button = InlineKeyboardButton(text=button_text, url=callback_url)
        markup.row(button)
        inline_keyboard = [[button] for button in markup.buttons]
        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    async def get_user_data(self):
        data = {}
        data['telegram_id'] = self.Crypto_Bot.message.chat.id
        if self.Crypto_Bot.message.from_user.username:
            data['username'] = self.Crypto_Bot.message.from_user.username
        if self.Crypto_Bot.message.from_user.first_name:
            data['first_name'] = self.Crypto_Bot.message.from_user.first_name
        if self.Crypto_Bot.message.from_user.last_name:
            data['last_name'] = self.Crypto_Bot.message.from_user.last_name
        data['is_bot'] = self.Crypto_Bot.message.from_user.is_bot if self.Crypto_Bot.message.from_user.is_bot else False
        data['language_code'] = self.Crypto_Bot.message.from_user.language_code
        data['is_premium'] = self.Crypto_Bot.message.from_user.is_premium if self.Crypto_Bot.message.from_user.is_premium else False
        data['follower_crypto_ch'] = False
        return data


class CryptoBot:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.bot_methods = CryptoBotMethods(self)
        self.step = 1
        self.router = Router(name=__name__)
        # bot_info = asyncio.run(self.get_bot_name())
        # print(f"https://t.me/{bot_info}")
        pass

    async def get_bot_name(self):
        bot_name = await self.bot.get_me()
        return bot_name.username

    async def handlers(self):
        @self.dp.message(CommandStart())
        async def start(message: types.Message):
            self.message = message
            create_table_users()
            data = await self.bot_methods.get_user_data()
            print("user has been written") if insert_db(data) else print("user has NOT been written")
            await self.bot_methods.take_dialog()

        @self.dp.callback_query()
        async def callbacks(callback: types.CallbackQuery):
            pass

        @self.dp.message(F.NEW_CHAT_MEMBERS)
        async def handle_new_chat_members(message: types.Message):
            pass
        # Здесь можно добавить логику обработки запросов на вступление
        # Например, подтвердить запрос:
        # await bot.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
        # Или отклонить запрос:
        # await bot.decline_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)

        await self.dp.start_polling(self.bot)

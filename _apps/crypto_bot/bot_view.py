import asyncio
from typing import Any

from aiogram import types, Router
from aiogram.dispatcher import router
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder

from crypto_bot import variables

class CryptoBotMethods:
    def __init__(self, Crypto_Bot):
        self.Crypto_Bot = Crypto_Bot
        self.min_per_hour = 2

    async def take_dialog(self):
        await self.Crypto_Bot.bot.send_message(self.Crypto_Bot.message.chat.id, 'TEST')
        for step in range(1, len(variables.media_way)+1):
            content = variables.media_way[step]
            await self.public_content(content)

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


class CryptoBot:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.bot_methods = CryptoBotMethods(self)
        self.step = 1
        self.router = Router(name=__name__)
        print("https://t.me/crypto_simple_bot")

    async def handlers(self):
        @self.dp.message(CommandStart())
        async def start(message: types.Message):
            self.message = message
            await self.bot_methods.take_dialog()

        @self.dp.callback_query()
        async def callbacks(callback: types.CallbackQuery):
            pass

        @self.router.chat_join_request()
        async def chat_join_request_handler(chat_join_request: types.ChatJoinRequest) -> Any:
            """
            Catch join requests
            """
            pass

        await self.dp.start_polling(self.bot)

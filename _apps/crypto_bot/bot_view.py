import asyncio
import time
from typing import Any
from _apps.crypto_bot.db.db_methods import create_table_users, insert_db, update_db, select_from, check_table_exists
from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest, BotCommand, \
    BotCommandScopeDefault
from aiogram.utils.keyboard import InlineKeyboardBuilder
from _apps.crypto_bot import variables
from _apps.excel_report import excel_compose
from _apps.crypto_bot.help_command import owner_help
from _apps.crypto_bot.set_commands_bot import commands
from datetime import datetime
from _apps.crypto_bot.variables import admin_id
from _apps.crypto_bot.test.is_working import IsWorking

class CryptoBotMethods:
    def __init__(self, Crypto_Bot):
        self.Crypto_Bot = Crypto_Bot
        self.min_per_hour = variables.min_per_hour

    async def is_subscribed(self, chat_id=variables.crypto_channel_id, **kwargs) -> bool:
        if kwargs.get('user_id') and kwargs['user_id']:
            user_id = kwargs['user_id']
        else:
            return False
        await self.set_log('\nIS_SUBSCRIBER: ', str(user_id))

        try:
            chat_member = await self.Crypto_Bot.bot.get_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )
            if chat_member.status in ["member", "creator"]:
                await self.set_log('\nIS_SUBSCRIBER: ', str(user_id), 'YES', '\n')
                return True
            else:
                await self.set_log('\nIS_SUBSCRIBER: ', str(user_id), 'NO', '\n')
                return False
        except Exception as ex:
            await self.set_log("IS SUBSCRIBER ERROR: ", str(ex))
            return False

    async def take_dialog(self, message):
        for step in range(1, len(variables.media_way)+1):
            if not await self.is_subscribed(user_id=message.chat.id):
                await self.Crypto_Bot.bot.send_message(int(admin_id), f"the user {message.chat.id} pressed start. Not subscribed to the channel")
                content = variables.media_way[step]
                await self.public_content(message, content)
            else:
                if step < 2:
                    await self.Crypto_Bot.bot.send_message(int(admin_id), f"the user {message.chat.id} pressed start. Subscribed to the channel")
                    await self.Crypto_Bot.bot.send_message(message.chat.id, variables.you_are_subscribed)
                await self.set_log('break')
                break

    async def public_content(self, message, content):
        markup = None
        await self.set_log("CONTENT GO TO ", str(message.from_user.id))
        for key in content:
            match key:
                case "video_notes":
                    for note in content[key]:
                        file = FSInputFile(note)
                        await self.Crypto_Bot.bot.send_video_note(message.chat.id, video_note=file)
                case "videos":
                    if len(content[key]) > 1:
                        media_group = []
                        for video_path in content[key]:
                            media_group.append(types.InputMediaVideo(media=FSInputFile(video_path)))
                        await self.Crypto_Bot.bot.send_media_group(message.chat.id, media=media_group)
                    elif content[key]:
                        file = FSInputFile(content[key][0])
                        await self.Crypto_Bot.bot.send_video(message.chat.id, video=file)
                case "pictures":
                    if len(content[key]) > 1:
                        media_group = []
                        for photo_path in content[key]:
                            media_group.append(types.InputMediaPhoto(media=FSInputFile(photo_path)))
                        await self.Crypto_Bot.bot.send_media_group(message.chat.id, media=media_group)
                    elif content[key]:
                        file = FSInputFile(content[key][0])
                        await self.Crypto_Bot.bot.send_photo(message.chat.id, photo=file)
                case "button":
                    markup = await self.get_markdown(content['button']['text'], content['button']['url'])
                case "texts":
                    for text in content[key]:
                        if markup and content[key].index(text) == len(content[key])-1:
                            await self.Crypto_Bot.bot.send_message(message.chat.id, text, reply_markup=markup, disable_web_page_preview=True)
                        else:
                            await self.Crypto_Bot.bot.send_message(message.chat.id, text, disable_web_page_preview=True)
                case 'timer':
                    if content['timer']:
                        await self.set_log('sleep content[timer]', str(content['timer']))
                        await asyncio.sleep(content['timer'] * self.min_per_hour)

    async def get_markdown(self, button_text, callback_url):
        markup = InlineKeyboardBuilder()
        button = InlineKeyboardButton(text=button_text, url=callback_url)
        markup.row(button)
        inline_keyboard = [[button] for button in markup.buttons]
        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    async def get_user_data(self, message, **kwargs):
        from_user = kwargs['from_user'] if kwargs.get('from_user') and kwargs['from_user'] else message.from_user
        data = {}
        data['telegram_id'] = from_user.id
        if from_user.username:
            data['username'] = from_user.username
        if from_user.first_name:
            data['first_name'] = from_user.first_name
        if from_user.last_name:
            data['last_name'] = from_user.last_name
        data['is_bot'] = from_user.is_bot if from_user.is_bot else False
        data['language_code'] = from_user.language_code
        data['is_premium'] = from_user.is_premium if from_user.is_premium else False
        data['follower_crypto_ch'] = True if await self.is_subscribed(user_id=from_user.id) else False
        if kwargs:
            for key in kwargs:
                if key in variables.fields_user_table:
                    data[key] = kwargs[key]
                else:
                    await self.set_log(f"key {key} is invalid")
        return data

    async def accept_join_request(self, request):
        await self.set_log(f"Join request {request.from_user.id}, waiting {variables.time_for_accept_join}")
        await asyncio.sleep(variables.time_for_accept_join)
        if await self.Crypto_Bot.bot.approve_chat_join_request(user_id=request.from_user.id, chat_id=request.chat.id):
            await self.set_log("CONGRATS ")
            await self.Crypto_Bot.bot.send_message(request.from_user.id, variables.join_message)
            return True
        return False

    async def update_join_status(self, request) -> Any:
        await self.set_log("user has been updated") if update_db(data={'follower_crypto_ch': True}, table=variables.user_table_name, telegram_id=request.from_user.id) else await self.set_log('user has been NOT updated')

    async def update_data(self, data, telegram_id) -> bool:
        try:
            update_db(data=data, table=variables.user_table_name, telegram_id=telegram_id)
            return True
        except Exception as ex:
            await self.set_log("update_join_status: ", str(ex))
            return False

    async def send_file(self, message, file_path, caption=variables.caption_send_file):
        file = FSInputFile(path=file_path)
        await self.Crypto_Bot.bot.send_document(message.chat.id, file, caption=caption)

    async def prepare_users_report(self, message) -> None:
        data = select_from(table=variables.user_table_name)
        report_excel_dict = await excel_compose.excel_compose_dict(data, fields=variables.fields_user_table)
        file_path = await excel_compose.write_to_excel(report_excel_dict, variables.sending_report_file_name)
        await self.send_file(message, file_path)

    async def insert(self, message, **kwargs):
        data = await self.get_user_data(message, **kwargs)
        if insert_db(data):
            await self.set_log(f"user {message.from_user.id} has been written")
            return True
        else:
            await self.set_log(f"user {message.from_user.id} has NOT been written")
            return False

    async def chat_join_request(self, request):
        if not check_table_exists():
            create_table_users()

        await self.insert(message=request)
        if request.invite_link.name:
            await self.set_log(f"Invite LINK name: ", str(request.invite_link.name))
            try:
                await self.update_data(data={'utm_chat': request.invite_link.name}, telegram_id=request.from_user.id)
            except Exception as ex:
                await self.set_log("INSERT", str(ex))
        if not await self.is_subscribed(user_id=request.user_chat_id):
            if await self.accept_join_request(request):
                await self.update_join_status(request)
                await self.Crypto_Bot.bot.send_message(int(admin_id), f"!!! the user {request.from_user.id} just subscribed to the channel")


    async def set_log(self, *args) -> Any:
        with open(variables.logs_path, 'a') as file:
            file.write(", ".join(args) + '\n')
        print(", ".join(args))

class CryptoBotVer3:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.bot_methods = CryptoBotMethods(self)
        self.step = 1
        self.router = Router(name=__name__)
        self.join_success = False
        print("https://t.me/Ferrari_forex_bot")

    async def set_commands(self):
        await self.bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())

    async def handlers(self):
        asyncio.create_task(IsWorking(self).send_message_schedule())

        await self.bot_methods.set_log(f"\n------------- {datetime.now().strftime('%Y-%M-%d %h:%m')} ----------------")
        await self.set_commands()

        @self.dp.message(Command("users"))
        async def users(message: types.Message):
            await self.bot_methods.prepare_users_report(message)

        @self.dp.message(Command("description"))
        async def description(message: types.Message):
            await self.bot.send_message(message.chat.id, owner_help)

        @self.dp.message(Command("logs"))
        async def users(message: types.Message):
            await self.bot_methods.send_file(message, file_path=variables.logs_path)

        @self.dp.message(CommandStart())
        async def start(message: types.Message):
            await self.bot_methods.set_log("USER STARTED: ", str(message.chat.id))
            # await self.bot_methods.update_message(message)
            utm_bot = "-"
            try:
                utm_bot = message.text.split(' ')[1] if message.text else None
            except Exception as ex:
                await self.bot_methods.set_log("utm_bot: ", str(ex))
            create_table_users()
            data = await self.bot_methods.get_user_data(message, utm_bot=utm_bot)
            await self.bot_methods.set_log(f"USER {message.from_user.id} has been written") if insert_db(data) else await self.bot_methods.set_log(f"USER {message.from_user.id} has NOT been written")
            await self.bot_methods.take_dialog(message)

        @self.dp.chat_join_request()
        async def chat_join_request_handler(request: ChatJoinRequest) -> Any:
            await self.bot_methods.chat_join_request(request)

        @self.dp.callback_query()
        async def callbacks(callback: types.CallbackQuery):
            pass

        await self.dp.start_polling(self.bot)

import asyncio
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

class CryptoBotMethods:
    def __init__(self, Crypto_Bot):
        self.Crypto_Bot = Crypto_Bot
        self.min_per_hour = 2

    async def is_subscribed(self, chat_id=variables.crypto_channel_id, **kwargs) -> bool:
        if kwargs.get('user_id') and kwargs['user_id']:
            user_id = kwargs['user_id']
        else:
            user_id = self.Crypto_Bot.message.chat.id
        try:
            chat_member = await self.Crypto_Bot.bot.get_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )
            if chat_member.status in ["member", "creator"]:
                return True
            else:
                return False
        except Exception as ex:
            print("IS SUBSCRIBER: ", ex)
            return False

    async def take_dialog(self):
        for step in range(1, len(variables.media_way)+1):
            if not await self.is_subscribed():
                content = variables.media_way[step]
                await self.public_content(content)
            else:
                if step < 2:
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

    async def get_markdown(self, button_text, callback_url):
        markup = InlineKeyboardBuilder()
        button = InlineKeyboardButton(text=button_text, url=callback_url)
        markup.row(button)
        inline_keyboard = [[button] for button in markup.buttons]
        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    async def get_user_data(self, **kwargs):
        from_user = kwargs['from_user'] if kwargs.get('from_user') and kwargs['from_user'] else self.Crypto_Bot.message.from_user
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
                    print(f"key {key} is invalid")
        return data

    async def accept_join_request(self, request):
        print(f"Join request, waiting {variables.time_for_accept_join}")
        await asyncio.sleep(variables.time_for_accept_join)

        if await self.Crypto_Bot.bot.approve_chat_join_request(user_id=request.from_user.id, chat_id=request.chat.id):
            await self.Crypto_Bot.bot.send_message(request.from_user.id, variables.join_message)
            return True
        return False

    async def update_join_status(self, request) -> Any:
        print("user has been updated") if update_db(data={'follower_crypto_ch': True}, table=variables.user_table_name, telegram_id=request.from_user.id) else print('user has been NOT updated')

    async def update_data(self, data, telegram_id) -> bool:
        try:
            update_db(data=data, table=variables.user_table_name, telegram_id=telegram_id)
            return True
        except Exception as ex:
            print("update_join_status: ", ex)
            return False

    async def send_file(self, file_path, caption=variables.caption_send_file):
        file = FSInputFile(path=file_path)
        await self.Crypto_Bot.bot.send_document(self.Crypto_Bot.message.chat.id, file, caption=caption)

    async def prepare_users_report(self) -> None:
        data = select_from(table=variables.user_table_name)
        report_excel_dict = await excel_compose.excel_compose_dict(data, fields=variables.fields_user_table)
        file_path = await excel_compose.write_to_excel(report_excel_dict, variables.sending_report_file_name)
        await self.send_file(file_path)

    async def update_message(self, message) -> None:
        if not self.Crypto_Bot.message:
            self.Crypto_Bot.message = message

    async def insert(self, **kwargs):
        data = await self.get_user_data(**kwargs)
        if insert_db(data):
            print("user has been written")
            return True
        else:
            print("user has NOT been written")
            return False

    async def chat_join_request(self, request):
        if not check_table_exists():
            create_table_users()
        await self.insert(from_user=request.from_user)
        if request.invite_link.name:
            print(request.invite_link.name)
            try:
                await self.update_data(data={'utm_chat': request.invite_link.name}, telegram_id=request.from_user.id)
            except Exception as ex:
                print(ex)
        if not await self.is_subscribed(user_id=request.user_chat_id):
            if await self.accept_join_request(request):
                await self.update_join_status(request)


class CryptoBotVer3:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.bot_methods = CryptoBotMethods(self)
        self.step = 1
        self.router = Router(name=__name__)
        self.message = None
        self.join_success = False
        print("https://t.me/crypto_simple_bot")

    async def set_commands(self):
        commands = [
            BotCommand(
                command="users",
                description="add bot, usage '/users'",
            ),
            BotCommand(
                command="description",
                description="add bot, usage '/description'",
            ),
        ]
        await self.bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())

    async def handlers(self):

        await self.set_commands()

        @self.dp.message(Command("users"))
        async def users(message: types.Message):
            await self.bot_methods.update_message(message)
            await self.bot_methods.prepare_users_report()

        @self.dp.message(Command("description"))
        async def description(message: types.Message):
            await self.bot.send_message(message.chat.id, owner_help)

        @self.dp.message(CommandStart())
        async def start(message: types.Message):
            await self.bot_methods.update_message(message)
            utm_bot = "-"
            try:
                utm_bot = message.text.split(' ')[1] if message.text else None
            except Exception as ex:
                print("utm_bot: ", ex)
            create_table_users()
            data = await self.bot_methods.get_user_data(utm_bot=utm_bot)
            print("user has been written") if insert_db(data) else print("user has NOT been written")
            await self.bot_methods.take_dialog()

        @self.dp.chat_join_request()
        async def chat_join_request_handler(request: ChatJoinRequest) -> Any:
            await self.bot_methods.chat_join_request(request)

        @self.dp.callback_query()
        async def callbacks(callback: types.CallbackQuery):
            pass

        await self.dp.start_polling(self.bot)

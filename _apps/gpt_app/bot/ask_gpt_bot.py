import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from gpt import ask_gpt

config = configparser.ConfigParser()
config.read("./settings/config.ini")
token = config['BOT']['token']

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dialog = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Hey')
    dialog[message.chat.id] = [ask_gpt.set_prompt()]
    pass

@dp.message_handler(content_types=['text'])
async def get_text(message: types.Message):
    dialog[message.chat.id].append(message.text)
    dialog[message.chat.id].append(ask_gpt.send_request(dialog[message.chat.id]))
    await bot.send_message(message.chat.id, dialog[message.chat.id][-1])


executor.start_polling(dp, skip_updates=True)

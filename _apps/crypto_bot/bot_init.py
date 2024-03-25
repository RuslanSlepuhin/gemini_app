from configparser import ConfigParser
from telethon import TelegramClient
from crypto_bot import variables as var
from aiogram import Bot, Dispatcher, types, Router
from aiogram.fsm.storage.memory import MemoryStorage

def read_config():
    config = ConfigParser()
    config.read(var.config_path)
    return config

def start_crypto_bot():
    config = read_config()
    token = config['BOT']['token']
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())
    form_router = Router()
    dp.include_router(form_router)
    return bot, dp


def start_private_bot():
    config = read_config()
    api_id = config['PRIVATE_BOT']['api_id']
    api_hash = config['PRIVATE_BOT']['api_hash']
    session = config['PRIVATE_BOT']['session']
    client = TelegramClient(session, int(api_id), api_hash)
    client.start()
    return client

if __name__ == "__main__":
    # start_private_bot()
    bot, dp = start_crypto_bot()
    from crypto_bot.bot_view import CryptoBot
    cp = CryptoBot([bot, dp])
    cp.handlers()
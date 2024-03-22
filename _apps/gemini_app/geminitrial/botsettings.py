import os
from telebot import TeleBot

token = os.getenv("TELEGRAM_TOKEN")
bot = TeleBot(token)
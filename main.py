import asyncio
import subprocess
from multiprocessing import Process

from _apps.crypto_bot import bot_init


def gemini_bot():
    from _apps.gemini_app.geminitrial import geminibot


def gemini_api():
    from _apps.gemini_app.api import api_gemini


def simpleatom_start():
    command = 'python _apps/simpleatom/manage.py runserver'
    process = subprocess.Popen(command, shell=True)
    process.communicate()

def crypto_bot():
    bot, dp = bot_init.start_crypto_bot()
    from _apps.crypto_bot.bot_view import CryptoBotVer3
    cp = CryptoBotVer3(bot, dp)
    asyncio.run(cp.handlers())


if __name__ == "__main__":
    # p1 = Process(target=gemini_bot, args=())
    # p2 = Process(target=gemini_api, args=())
    # p3 = Process(target=simpleatom_start, args=())
    p4 = Process(target=crypto_bot, args=())

    # p1.start()
    # p2.start()
    # p3.start()
    p4.start()

    # p1.join()
    # p2.join()
    # p3.join()
    p4.join()

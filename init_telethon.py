def real_estate_bot():
    from _apps.real_estate_bot.view import TelegramBot
    tb = TelegramBot()
    tb.connect_client()

if __name__ == '__main__':
    real_estate_bot()
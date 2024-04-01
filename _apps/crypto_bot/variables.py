crypto_channel_id = -1002072165211
you_are_subscribed = "You are already subscribed to the channel"
db_path = "./_apps/crypto_bot/db/crypto_users.sqlite3"

config_path = "./_apps/crypto_bot/settings/config.ini"
# invite_link = "https://t.me/+ZXRWq4EF6pQxMDMy"
invite_link = "https://t.me/+BODz1bR09AJlMjIy"
invite_links = {
    "main": "https://t.me/Message_Ferrari",
    "mainbot": "https://t.me/Juliaferraribot?start=mainbot",
}
media_path = "./_apps/crypto_bot/media/"
time_for_accept_join = 15
min_per_hour = 60
join_message = f"Congratulations🎉\n" \
               f"You got an free access to my\n" \
               f"FOREX TG COMMUNITY🔥\n\n" \
               f"✅ To get an access to my profitable ROBOT\n" \
               f"just text me right now 👉{invite_links['main']} 'ROBOT'"

text_step1 = f"To get an access to my ROBOT with an average monthly income of 25%, subscribe to my FREE Telegram channel: {invite_links['mainbot']}🤑\n\nJust click the button below: ⬇️⬇️⬇️"
text_step2 = f"💵 THAT'S MY LIFE 💵\n\n" \
             f"While I Chill And Have Fun - FerrariBot Makes Me Money 24/7 📈 Thanks Ferrari bot for my incredible routine.\n\n" \
             f"▶️Do you want to change your life for the better? 🙋‍♀️🙋🙋‍♂️\n\n" \
             f"Subscribe to my FREE Telegram channel RIGHT NOW {invite_links['mainbot']}  and I promise you will start to make money shortly🔥🔥🔥\n\n" \
             f"CLICK ON THE BUTTON BELOW ⬇️⬇️⬇️"
text_step3 = f"🤑MY MONTH RESULT 🤑\n\n" \
             f"📈 In March  my trading robot brought me:\n" \
             f"➡️ +31% profit\n\n" \
             f"🔥My development team and I have done a great job, and this is not the end. We improve our algorithms every day, more profit, less risks.🔥\n" \
             f"You missed another day and great opportunity of passive income with my trading robot again.😒\n\n" \
             f"‼️ATTENTION\n" \
             f"SUBSCRIBE TO MY FREE CHANNEL {invite_links['mainbot']} or\n" \
             f"CLICK ON THE BUTTON BELOW 👇👇👇👇"
text_step4 = f"📹Look through several video reviews out of hundreds that my subscribers send every day\n\n" \
             f"If you want to join our community and HAVE PASSIVE INCOME every day, YOU SHOULD SUBSCRIBE TO MY FREE CHANNEL {invite_links['mainbot']} RIGHT NOW💸\n\n" \
             f"or\n\nCLICK ON THE BUTTON BELOW 👇👇👇"
text_step5_1 = f"I want to answer the most common questions asked by newcomers:\n\n1. I don't have a lot of capital, will I be able to earn? 🤔\n\n" \
               f"Yes sure, you can start with the minimum and then increase the amount to get more profit. 500 usd is the minimum amount required for optimal robot performance.\n\n" \
               f"2. Why am I unable to link you to a demo account? ⏱️\n\n" \
               f"The robot algorithms do not run on a demo account. But why do you want to waste your time when you can connect the robot to a live account and start earning right away?\n\n" \
               f"3. Is it possible to withdraw money at any time? 💸\n\n" \
               f"Yes, there is no restrictions but usually people don't withdraw the profit and use it to make even more profit, " \
               f"because the more equity you have the bigger lot size the robot chooses and you get more profit."
text_step5_2 = f"🔥Hey! VERY SOON I WILL ANNOUNCE ABOUT OPENING NEW AVAILIABLE SEATS FOR CONNECTION TO MY TRADING ROBOT🚨Hurry up!\n\n" \
               f"⛔️ATTENTION⛔️\n\n" \
               f"SUBSCRIBE TO MY FREE CHANNEL {invite_links['mainbot']} or\nCLICK ON THE BUTTON BELOW 👇👇👇"

timers = {
    1: 5,
    2: 24*60,
    3: 0,
    4: 0,
    5: 0,
}

media_way = {
    1: {
        'video_notes': [media_path + "/ferrari/Julia_note_1.mp4"],
        'videos': [],
        'pictures': [],
        'button': {'text': 'Subscribe to the FREE channel 🎉', 'url': invite_links['mainbot']},
        'texts': [text_step1],
        'timer': timers[1]
    },
    2: {
        'video_notes': [media_path + "/ferrari/note2_Ferrari.mp4"],
        'videos': [],
        'pictures': [],
        'button': {'text': 'Subscribe to the FREE channel 🎉', 'url': invite_links['mainbot']},
        'texts': [text_step2],
        'timer': timers[2]
    },
    3: {
        'video_notes': [media_path + "/ferrari/Julia_note_2.mp4"],
        'videos': [],
        'pictures': [media_path + '/ferrari/post3_ferrari.jpg'],
        'button': {'text': 'Subscribe to the FREE channel 🎉', 'url': invite_links['mainbot']},
        'texts': [text_step3],
        'timer': timers[3]
    },
    # 4: {
    #     'video_notes': [],
    #     'videos': [media_path + 'Video_4-1.mp4', media_path + 'Video_4-2.mp4', media_path + 'Video_4-3.mp4', media_path + 'Video_4-4.mp4'],
    #     'pictures': [],
    #     'button': {'text': 'Subscribe to the FREE channel 🎉', 'url': invite_links['mainbot']},
    #     'texts': [text_step4],
    #     'timer': timers[4]
    # },
    # 5: {
    #     'video_notes': [],
    #     'videos': [],
    #     'pictures': [media_path + 'photo_5-1.jpg'],
    #     'button': {'text': 'Subscribe to the FREE channel 🎉', 'url': invite_links['mainbot']},
    #     'texts': [text_step5_1, text_step5_2],
    #     'timer': timers[5]
    # }
}

user_table_name = 'users'
user_table_create = f"CREATE TABLE IF NOT EXISTS {user_table_name} (" \
                    f"id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    f"telegram_id INT NOT NULL UNIQUE, " \
                    f"username VARCHAR(100), " \
                    f"first_name VARCHAR(100), " \
                    f"last_name VARCHAR(100), " \
                    f"is_bot BOLL, " \
                    f"language_code VARCHAR(10), " \
                    f"is_premium BOOL, " \
                    f"utm_bot VARCHAR(50), " \
                    f"utm_chat VARCHAR(50), " \
                    f"follower_crypto_ch BOOL);"

fields_user_table = ["id", "telegram_id", "username", "first_name", "last_name", "is_bot", "language_code", "is_premium", "utm_bot", "utm_chat", "follower_crypto_ch"]
get_users_from_db_query = f"SELECT * FROM {user_table_name}"
caption_send_file = "Report"
sending_report_file_name = "./_apps/crypto_bot/reports/report.xlsx"
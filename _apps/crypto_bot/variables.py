config_path = "./crypto_bot/settings/config.ini"
invite_link = "https://t.me/+vzPuOZD8spFhZWUy"
media_path = "./crypto_bot/media/"

text_step1 = f"To get an access to my profitable ROBOT you should subscribe to my FREE Telegram channel {invite_link}\n\nJust click on the button below ⬇️⬇️⬇️"
text_step2 = f"💵 MY INCOME FOR THE WEEK 💵\n\n➡️ " \
             f"My trading robot earn more than\n10 391.53$ in a week for me.\n\n" \
             f"This is a phenomenal result that I and everyone else is used to 📈\n\n" \
             f"🔼Subscribe to my FREE Telegram channel RIGHT NOW {invite_link} and I promise you will start to make money shortly🔥🔥🔥\n\n" \
             f"CLICK ON THE BUTTON BELOW ⬇️⬇️⬇️"
text_step3 = f"🤑MY RESULT FOR TODAY🤑\n\n📈 For the incomplete trading day my trading robot brought me:\n➡️ 💲2️⃣ 3️⃣2️⃣1️⃣.0️⃣1️⃣\n\n" \
             "🔥My development team have done a great job, but this is not the limit. We monitor the performance of the algorithm on " \
             "a daily basis and make improvements, focusing on minimizing risks and increasing daily profits🔥\n\n" \
             "You missed another day when you could have had passive income with my trading robot again 😒\n\n" \
             "⛔️ATTENTION⛔️\n\n" \
             f"SUBSCRIBE TO MY FREE CHANNEL {invite_link} or\nCLICK ON THE BUTTON BELOW 👇👇👇"
text_step4 = f"📹Look through several video reviews out of hundreds that my subscribers send every day\n\n" \
             f"If you want to join our community and HAVE PASSIVE INCOME every day, YOU SHOULD SUBSCRIBE TO MY FREE CHANNEL {invite_link} RIGHT NOW💸\n\n" \
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
               f"SUBSCRIBE TO MY FREE CHANNEL {invite_link} or\nCLICK ON THE BUTTON BELOW 👇👇👇"

media_way = {
    1: {
        'video_notes': [media_path + "video1.mp4"],
        'videos': [],
        'pictures': [],
        'button': {'text': '➡️Join FREE channel 🔥', 'url': invite_link},
        'texts': [text_step1],
        'timer': 2
    },
    2: {
        'video_notes': [],
        'videos': [],
        'pictures': [media_path + 'photo_2-1.jpg', media_path + 'photo_2-2.jpg', media_path + 'photo_2-3.jpg', media_path + 'photo_2-4.jpg', media_path + 'photo_2-5.jpg'],
        'button': {'text': '➡️Join FREE channel 💸', 'url': invite_link},
        'texts': [text_step2],
        'timer': 10
    },
    3: {
        'video_notes': [media_path + "video2.mp4"],
        'videos': [],
        'pictures': [media_path + 'photo_3-1.jpg'],
        'button': {'text': '➡️Join FREE channel 💸', 'url': invite_link},
        'texts': [text_step3],
        'timer': 15
    },
    4: {
        'video_notes': [],
        'videos': [media_path + 'Video_4-1.mp4', media_path + 'Video_4-2.mp4', media_path + 'Video_4-3.mp4', media_path + 'Video_4-4.mp4'],
        'pictures': [],
        'button': {'text': '➡️Join FREE channel 💸', 'url': invite_link},
        'texts': [text_step4],
        'timer': 5
    },
    5: {
        'video_notes': [],
        'videos': [],
        'pictures': [media_path + 'photo_5-1.jpg'],
        'button': {'text': '➡️Join FREE channel 💸', 'url': invite_link},
        'texts': [text_step5_1, text_step5_2],
        'timer': 0
    }
}
from multiprocessing import Process

def gemini_bot():
    from geminitrial import geminibot

def gemini_api():
    from api import api_gemini

if __name__ == "__main__":
    p1 = Process(target=gemini_bot, args=())
    p2 = Process(target=gemini_api, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()

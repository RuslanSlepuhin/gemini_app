import subprocess
from multiprocessing import Process

def gemini_bot():
    from _apps.gemini_app.geminitrial import geminibot


def gemini_api():
    from _apps.gemini_app.api import api_gemini


def simpleatom_start():
    command = 'python _apps/simpleatom/manage.py runserver'
    process = subprocess.Popen(command, shell=True)
    process.communicate()

if __name__ == "__main__":
    p1 = Process(target=gemini_bot, args=())
    p2 = Process(target=gemini_api, args=())
    p3 = Process(target=simpleatom_start, args=())

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

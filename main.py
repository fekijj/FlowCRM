# main.py
from threading import Thread
import webbrowser
import time
from backend.app import create_app
import asyncio
from backend.telegram_bot import run_bot
from backend.models import Base, engine
Base.metadata.create_all(engine)


def run_flask():
    app = create_app()
    app.run(host='127.0.0.1', port=5000)

def start_telegram():
    asyncio.run(run_bot())

if __name__ == '__main__':
    Thread(target=run_flask).start()
    Thread(target=start_telegram).start()

    time.sleep(2)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("База данных создана ✅")

# main.py
from threading import Thread
import webbrowser
import time
from backend.app import create_app
import asyncio
from backend.telegram_bot import run_bot
from backend.models import Base, engine, User, get_session
from backend.app import create_app
# Создание таблиц
Base.metadata.create_all(engine)

# Сид: админ
with get_session() as db:
    if not db.query(User).filter_by(login="admin").first():
        admin = User(name="Админ", login="admin", role="admin")
        admin.set_password("1234")
        db.add(admin)

# Flask и бот
def run_flask():
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)


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

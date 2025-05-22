# backend/telegram_bot.py
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

TOKEN = os.getenv("BOT_TOKEN", "7840807054:AAEwn_fKYh6NYzZJlMjLxNOukAYhiCjsey4")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())

@dp.message()
async def echo(message: Message):
    await message.answer("FlowCRM бот на связи ✅")

async def run_bot():
    await dp.start_polling(bot)

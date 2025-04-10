import logging
from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot("TOKEN", default = DefaultBotProperties(parse_mode = ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Помощь")

@dp.message()
async def echo(message: Message):
    await message.answer(message.text)

async def main() -> None:
    await bot.delete_webhook(True)
    await dp.start_polling(bot)

logging.basicConfig(level=logging.INFO)
run(main())

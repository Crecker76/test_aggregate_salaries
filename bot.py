import asyncio
import json

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message

import algoritm

TOKEN = 'YOUR TOKEN'
dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    """Обработка команды старт"""
    await message.answer(
        f"Hi {message.from_user.first_name}!"
    )


async def handle_json_payload(message: types.Message):
    try:
        payload = json.loads(message.text)
        dt_from = payload.get("dt_from")
        dt_upto = payload.get("dt_upto")
        group_type = payload.get("group_type")
        return dt_from, dt_upto, group_type
    except json.JSONDecodeError:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Невалидный запос. Пример запроса:\n{\"dt_from\": \"2022-09-01T00:00:00\", \"dt_upto\": \"2022-12-31T23:59:00\", \"group_type\": \"month\"}"
        )
    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text=f"Error processing payload: {e}")

@dp.message()
async def echo(message: types.Message):
    if message.text.startswith("{") and message.text.endswith("}"):
        dt_from, dt_upto, group_type = await handle_json_payload(message)
        result = algoritm.aggregate_salaries(algoritm.DATA, dt_from=dt_from, dt_upto=dt_upto, group_type=group_type)
        await message.answer(
            f'{result}'
        )
    else:
        await bot.send_message(chat_id=message.chat.id, text="Невалидный запос. Пример запроса:\n{\"dt_from\": \"2022-09-01T00:00:00\", \"dt_upto\": \"2022-12-31T23:59:00\", \"group_type\": \"month\"}")

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

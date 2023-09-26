from aiogram.types import Message
from aiogram import Bot, Dispatcher, F, Router
import asyncio

import openai

from config import BOT_TOKEN, CHATGPT_TOKEN

router = Router()


async def start() -> None:
    print('Bot is ready to work!')

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    openai.api_key = CHATGPT_TOKEN

    dp.include_router(router)

    await dp.start_polling(bot, skip_updates=True)


@router.message(F.text == '/start' or '/help')
async def skip_commands(*args):
    pass


@router.message()
async def send_to_chatgpt(msg: Message):
    prompt = [{'role': 'user', 'content': msg.text}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=1.2,
        max_tokens=2596)

    await msg.answer(text=response['choices'][0]['message']['content'])


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Bot stopped')

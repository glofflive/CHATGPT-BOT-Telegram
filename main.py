import openai
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import time
import random
import aiofiles
import aiofiles.os
from data.config import *

bot = Bot(token=BOT_TOKEN,parse_mode="html")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

openai.api_key = "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"

openaiapi_key1 = "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"

@dp.message_handler(commands="hello",state="*")
async def handlerwithjoinbotingroup(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(f"<b>Бот готов в работе, чтобы задать ИИ вопрос напишите</b>"
                        f"<code>/chat</code> <b>аргументы</b>"
                        f"<b>К примеру:</b> <code>/chat Какая погода в Казахстане?</code>")

@dp.message_handler(commands="start")
async def commandstart(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Добавить в чат", url="http://t.me/NewBrainingBot?startgroup=hello"))

        await message.answer(f"🤖 <code>{message.from_user.first_name}</code>, <b>Добрый день данный бот генерирует текст по аргументом. CHATGPT-3 самая умная ИИ, ждет пока ты ее добавишь в чат)</b>",reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text="Добавить в чат", url="http://t.me/NewBrainingBot?startgroup=hello"))

        await message.reply(f"<b>Бот готов в работе, чтобы задать ИИ вопрос напишите</b>"
                            f"<code>/chat</code> <b>аргументы</b>"
                            f"<b>К примеру:</b> <code>/chat Какая погода в Казахстане?</code>",reply_markup=keyboard)


@dp.message_handler(commands="chat")
async def chatgivegptresult(message: types.Message, state: FSMContext):

    if message.chat.type == 'private':
        await message.answer(f"Данная команда доступна только в чате!")
    else:
        currentTime = time.time()
        msgreply = await message.reply("<i>🌟 Загрузка...</i>\n<code>Это может занять некоторое время.</code>")
        prompt = message.text[6:]
        print(prompt)
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt,max_tokens=4000)
        print(response)
        ysa = response["choices"][0]["text"]
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Получить в TXT", callback_data="getxt"))
        await msgreply.edit_text(f"<i>Спроси тоже у ИИ свои вопросы: @NewBrainingBot </i>\n" + f"<code>{ysa}</code>",reply_markup=keyboard)
        await state.update_data(text=ysa)

@dp.callback_query_handler(text="getxt")
async def send_random_value(call: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        name = "get" + f"{call.from_user.id}" + f"{random.randint(1,5123)}"
        async with aiofiles.open(f'{name}.txt', mode='w') as handle:
            contents = await handle.write(data['text'])
            handle.close()


        await call.message.answer_document(open(f"{name}.txt", "rb"))
        await aiofiles.os.remove(f'{name}.txt')
    except:
        await call.message.answer(f"Ошибка")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print(f'{NAME} успешно запущен!!')
    asyncio.run(main())
import openai
from openai import OpenAI
from aiogram import types, Router, F
from aiogram.filters import Command
from collections import defaultdict

router = Router(name=__name__)

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

history_store = {}


@router.message(Command("ai"))
async def start_ai(message: types.Message):
    user_id = message.from_user.id
    history_store[user_id] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    await message.answer("💬 Введіть ваше запитання. Напишіть /end щоб завершити сесію.")


@router.message(F.text, ~Command("end"))
async def ai_respond(message: types.Message):
    user_id = message.from_user.id
    if user_id not in history_store:
        return await message.answer("❗ Спочатку надішліть /ai")

    history_store[user_id].append({"role": "user", "content": message.text})

    completion = client.chat.completions.create(
        messages=history_store[user_id],
        temperature=0.7,
        model="meta-llama-3.1-8b-instruct"
    )

    reply_text = completion.choices[0].message.content
    history_store[user_id].append({"role": "assistant", "content": reply_text})

    await message.answer(reply_text)


@router.message(Command("end"))
async def end_ai(message: types.Message):
    user_id = message.from_user.id
    history_store.pop(user_id, None)
    await message.answer("✅ Сесію завершено.")


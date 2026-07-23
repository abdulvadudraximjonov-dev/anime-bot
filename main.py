import asyncio
import logging
import os
from threading import Thread
import urllib.parse

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from deep_translator import GoogleTranslator
from flask import Flask
import requests

# ------------------------------------
# 1. RENDER UCHUN FLASK PORT SERVER
# ------------------------------------
app = Flask('')


@app.route('/')
def home():
  return 'Bot 24/7 ishlamoqda!'


def run():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = Thread(target=run)
  t.daemon = True
  t.start()


# Web-serverni ishga tushiramiz
keep_alive()

# ------------------------------------
# 2. TELEGRAM BOT SOZLAMALARI
# ------------------------------------
TOKEN ="8847420139:AAFj4COfVuZy2l6Xr6WfmkkIQ-kofg0fxMg"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# /start komandasi
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
  await message.answer(
      "Assalomu alaykum! Men Anime qidiruvchi botman. 🍿\n\n"
      "Menga istalgan anime nomini yozib yuboring (masalan: *Naruto*).",
      parse_mode='Markdown',
  )


# Anime qidirish
@dp.message()
async def search_anime(message: types.Message):
  query = message.text
  await message.answer("🔍 Qidirilmoqda, kuting...")

  url = f'https://shikimori.one/api/animes?search={query}&limit=1'
  headers = {'User-Agent': 'AnimeBot/1.0'}

  try:
    response = requests.get(url, headers=headers).json()

    if not response:
      await message.answer(
          "❌ Afsuski, bunday anime topilmadi. Nomini to'g'ri yozganingizni"
          ' tekshiring.'
      )
      return

    anime = response[0]
    anime_id = anime['id']

    detail_url = f'https://shikimori.one/api/animes/{anime_id}'
    detail = requests.get(detail_url, headers=headers).json()

    title_ru = detail.get('russian') or detail.get('name')
    title_eng = detail.get('name')
    episodes = detail.get('episodes', "Noma'lum")
    score = detail.get('score', 'Baholanmagan')
    status = detail.get('status', "Noma'lum")

    status_dict = {
        'released': 'Tugallangan 🏁',
        'ongoing': 'Davom etmoqda 🔄',
        'anons': 'Afisha / Anons 📣',
    }
    status_uz = status_dict.get(status, "Noma'lum")

    caption = (
        f'🎬 **Nomi:** {title_ru} ({title_eng})\n\n'
        f'⭐️ **Baho:** {score} / 10\n'
        f'📺 **Qismlar soni:** {episodes}\n'
        f'📌 **Holati:** {status_uz}'
    )

    image_url = f"https://shikimori.one{anime['image']['original']}"
    shikimori_url = f"https://shikimori.one{anime['url']}"

    search_query = urllib.parse.quote(f'{title_eng} anime uzbek tilida')
    watch_url = f'https://www.google.com/search?q={search_query}'

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🎬 Ko'rish / Tomosha qilish", url=watch_url
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📖 Tavsifni o'qish (O'zbekcha)",
            callback_data=f'desc_{anime_id}',
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🌐 Rasmiy saytda ko'rish", url=shikimori_url
        )
    )

    await message.answer_photo(
        photo=image_url,
        caption=caption,
        reply_markup=builder.as_markup(),
        parse_mode='Markdown',
    )

  except Exception as e:
    logging.error(f'Xatolik: {e}')
    await message.answer('⚠️ Qidiruv vaqtida xatolik yuz berdi.')


# Tavsif tugmasi bosilganda
@dp.callback_query(lambda c: c.data.startswith('desc_'))
async def show_description(callback_query: types.CallbackQuery):
  await callback_query.answer('⏳ Tavsif o\'zbek tiliga tarjima qilinmoqda...')

  anime_id = callback_query.data.split('_')[1]
  detail_url = f'https://shikimori.one/api/animes/{anime_id}'
  headers = {'User-Agent': 'AnimeBot/1.0'}

  try:
    detail = requests.get(detail_url, headers=headers).json()
    description = detail.get('description', 'Tavsif topilmadi.')

    if description and description != 'Tavsif topilmadi.':
      translator = GoogleTranslator(source='auto', target='uz')
      translated_desc = translator.translate(description)
    else:
      translated_desc = "Ushbu anime uchun tavsif mavjud emas."

    await callback_query.message.answer(
        f"📖 **Tavsif (O'zbekcha):**\n\n{translated_desc}",
        parse_mode='Markdown',
    )
  except Exception as e:
    logging.error(f'Tarjima xatosi: {e}')
    await callback_query.message.answer(
        "⚠️ Tavsifni yuklashda xatolik yuz berdi."
    )


async def main():
  await dp.start_polling(bot)


if __name__ == '__main__':
  asyncio.run(main())
                   

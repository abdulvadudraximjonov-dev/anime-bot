import os
from threading import Thread
import urllib.parse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from deep_translator import GoogleTranslator
from flask import Flask
import requests

# 1. FLASK SERVER
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


keep_alive()

# 2. BOT SOZLAMALARI
TOKEN = "8847420139:AAFj4COfVuZy2l6Xr6WfmkkIQ-kofg0fxMg"  # Botfather'dan olgan tokeningizni yozing

bot = Bot(token=TOKEN)
dp = Dispatcher()

HEADERS = {'User-Agent': 'AnimeUzBot/1.0'}


class UserState(StatesGroup):
  waiting_for_anime_name = State()


# 4 TA ASOSIY TUGMA
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔍 Top 15 Anime'),
            KeyboardButton(text='📰 Soʻnggi Yangiliklar'),
        ],
        [
            KeyboardButton(text='🇺🇿 Oʻzbekcha Tavsif'),
            KeyboardButton(text='🎬 Tomosha qilish'),
        ],
    ],
    resize_keyboard=True,
)


@dp.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
  await state.clear()
  await message.answer(
      'Assalomu alaykum! 👋\n\n'
      'Anime botimizga xush kelibsiz! Kerakli boʻlimni tanlang yoki anime nomini yozing:',
      reply_markup=main_keyboard,
  )


# 1. TOP 15 ANIME (SHIKIMORI BAZASI)
@dp.message(lambda m: m.text == '🔍 Top 15 Anime')
async def top_15_anime(message: types.Message):
  msg = await message.answer('⏳ Eng mashhur 15 ta anime yuklanmoqda...')
  try:
    url = 'https://shikimori.one/api/animes?limit=15&order=popularity'
    res = requests.get(url, headers=HEADERS, timeout=10)
    data = res.json()

    if not data:
      await msg.edit_text('❌ Maʻlumot olib boʻlmadi.')
      return

    text = '🔥 **Top 15 Eng Mashhur Animelar:**\n\n'
    for idx, item in enumerate(data, 1):
      name = item.get('russian') or item.get('name')
      score = item.get('score', 'N/A')
      text += f'{idx}. **{name}** — ⭐ {score}\n'

    text += (
        "\n💡 *Batafsil ma'lumot olish uchun anime nomini chatga yozing!*"
    )
    await msg.edit_text(text, parse_mode='Markdown')
  except Exception:
    await msg.edit_text('⚠️ Server bilan aloqa uzildi. Qayta urinib koʻring.')


# 2. SO'NGGI YANGILIKLAR (HOZIR EFIRDA KETAYOTGAN ANIMELAR)
@dp.message(lambda m: m.text == '📰 Soʻnggi Yangiliklar')
async def latest_news(message: types.Message):
  msg = await message.answer(
      '⏳ Bugungi va soʻnggi yangiliklar yuklanmoqda...'
  )
  try:
    url = 'https://shikimori.one/api/animes?limit=5&status=ongoing&order=popularity'
    res = requests.get(url, headers=HEADERS, timeout=10)
    data = res.json()

    if not data:
      await msg.edit_text('❌ Yangiliklar topilmadi.')
      return

    news_text = '📰 **Hozirda efirga uzatilayotgan eng soʻnggi animelar:**\n\n'

    for item in data:
      name = item.get('russian') or item.get('name')
      episodes = item.get('episodes_Aired', 0)
      score = item.get('score', 'N/A')

      news_text += (
          f'🎬 **{name}**\n📌 Chiqqan qismlari: {episodes}-qism\n⭐ Baho:'
          f' {score}\n\n---\n'
      )

    await msg.edit_text(news_text, parse_mode='Markdown')
  except Exception:
    await msg.edit_text('⚠️ Yangiliklarni yuklashda xatolik yuz berdi.')


# 3. O'ZBEKCHA TAVSIF
@dp.message(lambda m: m.text == '🇺🇿 Oʻzbekcha Tavsif')
async def uzbek_description_info(message: types.Message):
  await message.answer(
      '🇺🇿 **Oʻzbekcha Tavsif Boʻlimi**\n\n'
      'Istalgan anime haqida oʻzbekcha tavsif olish uchun chatga **anime nomini** yozing!\n'
      '💡 *Masalan:* `Naruto`, `Solo Leveling`, `Bleach`',
      parse_mode='Markdown',
  )


# 4. TOMOSHA QILISH
@dp.message(lambda m: m.text == '🎬 Tomosha qilish')
async def watch_anime_prompt(message: types.Message, state: FSMContext):
  await state.set_state(UserState.waiting_for_anime_name)
  await message.answer(
      '🎬 Qaysi animeni tomosha qilmoqchisiz?\n\n'
      'Iltimos, **anime nomini yozib yuboring** (masalan: `Naruto`):',
      parse_mode='Markdown',
  )


@dp.message(UserState.waiting_for_anime_name)
async def process_anime_watch_search(
    message: types.Message, state: FSMContext
):
  anime_name = message.text
  await state.clear()

  encoded_name = urllib.parse.quote(anime_name)
  watch_keyboard = InlineKeyboardMarkup(
      inline_keyboard=[[
          InlineKeyboardButton(
              text=f'🔍 Telegramdan "{anime_name}"ni topish',
              url=f'https://t.me/search?q={encoded_name}',
          )
      ]]
  )

  await message.answer(
      f'🍿 **{anime_name}** animesini Telegramdagi kanallardan tomosha qilish uchun tugmani bosing:',
      reply_markup=watch_keyboard,
      parse_mode='Markdown',
  )


# ANIME QIDIRUV VA TAVSIF
@dp.message()
async def search_and_translate(message: types.Message):
  query = message.text
  msg = await message.answer(f'🔍 *{query}* boʻyicha qidirilmoqda...')

  try:
    # Shikimori orqali qidirish
    search_url = (
        f'https://shikimori.one/api/animes?search={urllib.parse.quote(query)}&limit=1'
    )
    res = requests.get(search_url, headers=HEADERS, timeout=10)
    data = res.json()

    if not data:
      await msg.edit_text(
          f'❌ Afsuski, *{query}* nomli anime topilmadi.',
          parse_mode='Markdown',
      )
      return

    anime_id = data[0]['id']

    # Anime batafsil ma'lumotini olish
    detail_url = f'https://shikimori.one/api/animes/{anime_id}'
    detail_res = requests.get(detail_url, headers=HEADERS, timeout=10)
    anime = detail_res.json()

    title = anime.get('russian') or anime.get('name')
    score = anime.get('score', 'N/A')
    episodes = anime.get('episodes') or anime.get('episodes_Aired') or 'Noma\'lum'
    description = anime.get('description_source') or anime.get('description') or ''
    image_path = anime.get('image', {}).get('original')
    image_url = (
        f'https://shikimori.one{image_path}' if image_path else None
    )

    # Tavsifni tarjima qilish
    if description:
      try:
        translator = GoogleTranslator(source='auto', target='uz')
        translated_synopsis = translator.translate(description[:400])
      except:
        translated_synopsis = description[:400]
    else:
      translated_synopsis = 'Tavsif mavjud emas.'

    caption = (
        f'🎬 **{title}**\n\n'
        f'⭐ **Baho:** {score}\n'
        f'🎞 **Qismlar:** {episodes}\n\n'
        f'📝 **Oʻzbekcha Tavsif:**\n{translated_synopsis}...'
    )

    encoded_title = urllib.parse.quote(title)
    watch_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text='🎬 Telegramda tomosha qilish',
                url=f'https://t.me/search?q={encoded_title}',
            )
        ]]
    )

    await msg.delete()

    if image_url:
      await message.answer_photo(
          photo=image_url,
          caption=caption,
          reply_markup=watch_keyboard,
          parse_mode='Markdown',
      )
    else:
      await message.answer(
          caption, reply_markup=watch_keyboard, parse_mode='Markdown'
      )

  except Exception:
    await msg.edit_text('❌ Qidiruvda vaqtinchalik xatolik yuz berdi.')


if __name__ == '__main__':
  import asyncio

  asyncio.run(dp.start_polling(bot))

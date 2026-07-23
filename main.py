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

# 1. RENDER UCHUN FLASK PORT SERVER
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
TOKEN = "8847420139:AAFj4COfVuZy2l6Xr6WfmkkIQ-kofg0fxMg"  # BotFather'dan olingan tokeningizni kiriting

bot = Bot(token=TOKEN)
dp = Dispatcher()


# FSM Holatlari
class UserState(StatesGroup):
  waiting_for_anime_name = State()


# MAIN PASTA TURADIGAN 4 TA TUGMA
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


# /start komandasi
@dp.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
  await state.clear()
  await message.answer(
      'Assalomu alaykum! 👋\n\n'
      'Anime botimizga xush kelibsiz. Kerakli boʻlimni tanlang yoki anime nomini yozing:',
      reply_markup=main_keyboard,
  )


# 1-TUGMA: TOP 15 SIFATLI ANIME
@dp.message(lambda m: m.text == '🔍 Top 15 Anime')
async def top_15_anime(message: types.Message):
  await message.answer('⏳ Eng sifatli 15 ta anime yuklanmoqda...')
  try:
    url = 'https://api.jikan.moe/v4/top/anime?limit=15'
    response = requests.get(url).json().get('data', [])

    text = '🔥 **Top 15 Eng Sifatli Animelar:**\n\n'
    for idx, item in enumerate(response, 1):
      title = item.get('title')
      score = item.get('score', 'N/A')
      text += f'{idx}. **{title}** — ⭐ {score}\n'

    text += (
        "\n💡 *Batafsil ma'lumot va tavsifini ko'rish uchun anime nomini chatga"
        ' yozing!*'
    )
    await message.answer(text, parse_mode='Markdown')
  except Exception:
    await message.answer('Maʼlumot olishda xatolik yuz berdi.')


# 2-TUGMA: SO'NGGI YANGILIKLAR
@dp.message(lambda m: m.text == '📰 Soʻnggi Yangiliklar')
async def latest_news(message: types.Message):
  await message.answer('⏳ Bugungi va soʻnggi yangiliklar yuklanmoqda...')
  try:
    url = 'https://api.jikan.moe/v4/seasons/now?limit=3'
    response = requests.get(url).json().get('data', [])

    translator = GoogleTranslator(source='en', target='uz')
    news_text = '📰 **Oʻsha kuni / Hozirgi mavsumda chiqqan yangiliklar:**\n\n'

    for item in response:
      title = item.get('title')
      synopsis = item.get('synopsis', 'Tavsif yoq')[:150]

      try:
        translated_synopsis = translator.translate(synopsis)
      except:
        translated_synopsis = synopsis

      news_text += f'🎬 **{title}**\n📝 {translated_synopsis}...\n\n---\n'

    await message.answer(news_text, parse_mode='Markdown')
  except Exception:
    await message.answer('Yangiliklarni yuklashda xatolik yuz berdi.')


# 3-TUGMA: O'ZBEKCHA TAVSIF
@dp.message(lambda m: m.text == '🇺🇿 Oʻzbekcha Tavsif')
async def uzbek_description_info(message: types.Message):
  await message.answer(
      '🇺🇿 **Oʻzbekcha Tavsif Boʻlimi**\n\n'
      'Istalgan anime haqida oʻzbekcha tavsif va maʼlumot olish uchun chatga **anime nomini** yozib yuboring!\n'
      '💡 *Masalan:* `Naruto`, `Solo Leveling`, `Attack on Titan`',
      parse_mode='Markdown',
  )


# 4-TUGMA: TOMOSHA QILISH (ANIME NOMINI SO'RASH)
@dp.message(lambda m: m.text == '🎬 Tomosha qilish')
async def watch_anime_prompt(message: types.Message, state: FSMContext):
  await state.set_state(UserState.waiting_for_anime_name)
  await message.answer(
      '🎬 Qaysi animeni tomosha qilmoqchisiz?\n\n'
      'Iltimos, **anime nomini yozib yuboring** (masalan: `Naruto` yoki `Solo Leveling`):',
      parse_mode='Markdown',
  )


# HAR QANDAY KANALDA QIDIRISH HAVOLASINI YASASH
@dp.message(UserState.waiting_for_anime_name)
async def process_anime_watch_search(
    message: types.Message, state: FSMContext
):
  anime_name = message.text
  await state.clear()

  # Telegram global qidiruv havolasi
  encoded_name = urllib.parse.quote(anime_name)
  telegram_search_url = f'https://t.me/s/{encoded_name}'
  global_search_url = f'https://t.me/share/url?url=https://t.me/search?q={encoded_name}&text=Anime:%20{encoded_name}'

  watch_keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text=f'🔍 Telegramdan "{anime_name}"ni topish',
                  url=f'https://t.me/search?q={encoded_name}',
              )
          ]
      ]
  )

  await message.answer(
      f'🍿 **{anime_name}** animesini Telegramdagi istalgan kanaldan tomosha qilish uchun quyidagi tugmani bosing:',
      reply_markup=watch_keyboard,
      parse_mode='Markdown',
  )


# ODDIY MATN YOZILGANDA ANIME QIDIRISH
@dp.message()
async def search_and_translate(message: types.Message):
  query = message.text
  await message.answer(
      f'🔍 *{query}* boʻyicha qidirilmoqda va tavsif oʻzbekchaga tarjima'
      ' qilinmoqda...'
  )

  try:
    url = f'https://api.jikan.moe/v4/anime?q={query}&limit=1'
    response = requests.get(url).json().get('data', [])

    if not response:
      await message.answer('❌ Afsuski, bunday anime topilmadi.')
      return

    anime = response[0]
    title = anime.get('title')
    score = anime.get('score', 'N/A')
    episodes = anime.get('episodes', 'Noma\'lum')
    synopsis = anime.get('synopsis', 'Tavsif yoʻq')
    image_url = anime.get('images', {}).get('jpg', {}).get('image_url')

    translator = GoogleTranslator(source='en', target='uz')
    try:
      translated_synopsis = translator.translate(synopsis[:500])
    except:
      translated_synopsis = synopsis

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
    await message.answer('Qidiruvda xatolik yuz berdi.')


if __name__ == '__main__':
  import asyncio

  asyncio.run(dp.start_polling(bot))
  

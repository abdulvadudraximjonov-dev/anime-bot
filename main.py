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

# 1. FLASK PORT SERVER
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
TOKEN = "8847420139:AAFj4COfVuZy2l6Xr6WfmkkIQ-kofg0fxMg"  # BotFather tokeningiz
CHANNEL_USERNAME = "@Ongoing animelar"  # Masalan: @anime_uz_kanali
CHANNEL_URL = "https://t.me/anime_team_01"  # Kanal havolasi

bot = Bot(token=TOKEN)
dp = Dispatcher()
HEADERS = {'User-Agent': 'AnimeUzBot/1.0'}


class UserState(StatesGroup):
  waiting_for_anime_name = State()


# TUGMALAR MENYUSI
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔍 Top 15 Anime'),
            KeyboardButton(text='📰 Soʻnggi Yangiliklar'),
        ],
        [
            KeyboardButton(text='🎲 Tasodifiy Anime'),
            KeyboardButton(text='🎬 Tomosha qilish'),
        ],
        [
            KeyboardButton(text='🇺🇿 Oʻzbekcha Tavsif'),
            KeyboardButton(text='📢 Kanalimiz'),
        ],
    ],
    resize_keyboard=True,
)


# OBUNANI TEKSHIRISH FUNKSIYASI
async def check_sub(user_id: int) -> bool:
  try:
    member = await bot.get_chat_member(
        chat_id=CHANNEL_USERNAME, user_id=user_id
    )
    if member.status in ['creator', 'administrator', 'member']:
      return True
    return False
  except Exception:
    return True  # Kanal sozlanmagan bo'lsa o'tkazib yuboradi


# /start KOMANDASI
@dp.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
  await state.clear()
  is_subbed = await check_sub(message.from_user.id)

  if not is_subbed:
    sub_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='📢 Kanalga obuna boʻlish', url=CHANNEL_URL
                )
            ],
            [
                InlineKeyboardButton(
                    text='✅ Obunani tekshirish', callback_data='check_subscription'
                )
            ],
        ]
    )
    await message.answer(
        '👋 Botdan foydalanish uchun avval kanalimizga obuna boʻling:',
        reply_markup=sub_keyboard,
    )
    return

  await message.answer(
      'Assalomu alaykum! 👋\nAnime botimizga xush kelibsiz! Boʻlimni tanlang:',
      reply_markup=main_keyboard,
  )


# OBUNANI TEKSHIRISH TUGMASI (CALLBACK)
@dp.callback_query(lambda c: c.data == 'check_subscription')
async def callback_check_sub(callback_query: types.CallbackQuery):
  is_subbed = await check_sub(callback_query.from_user.id)
  if is_subbed:
    await callback_query.message.delete()
    await callback_query.message.answer(
        '✅ Rahmat! Endi botdan toʻliq foydalanishingiz mumkin.',
        reply_markup=main_keyboard,
    )
  else:
    await callback_query.answer('❌ Hali kanalga obuna boʻlmadingiz!', show_alert=True)


# 1. TOP 15 ANIME
@dp.message(lambda m: m.text == '🔍 Top 15 Anime')
async def top_15_anime(message: types.Message):
  msg = await message.answer('⏳ Yuklanmoqda...')
  try:
    res = requests.get(
        'https://shikimori.one/api/animes?limit=15&order=popularity',
        headers=HEADERS,
        timeout=10,
    )
    data = res.json()

    text = '🔥 **Top 15 Eng Mashhur Animelar:**\n\n'
    for idx, item in enumerate(data, 1):
      name = item.get('russian') or item.get('name')
      score = item.get('score', 'N/A')
      text += f'{idx}. **{name}** — ⭐ {score}\n'

    await msg.edit_text(text, parse_mode='Markdown')
  except Exception:
    await msg.edit_text('⚠️ Xatolik yuz berdi.')


# 2. SO'NGGI YANGILIKLAR
@dp.message(lambda m: m.text == '📰 Soʻnggi Yangiliklar')
async def latest_news(message: types.Message):
  msg = await message.answer('⏳ Yuklanmoqda...')
  try:
    res = requests.get(
        'https://shikimori.one/api/animes?limit=5&status=ongoing&order=popularity',
        headers=HEADERS,
        timeout=10,
    )
    data = res.json()

    news_text = '📰 **Hozirda efirga uzatilayotgan animelar:**\n\n'
    for item in data:
      name = item.get('russian') or item.get('name')
      episodes = item.get('episodes_Aired', 0)
      score = item.get('score', 'N/A')
      news_text += (
          f'🎬 **{name}**\n📌 Chiqqan qismi: {episodes}\n⭐ Baho:'
          f' {score}\n\n---\n'
      )

    await msg.edit_text(news_text, parse_mode='Markdown')
  except Exception:
    await msg.edit_text('⚠️ Xatolik yuz berdi.')


# 3. TASODIFIY ANIME (YANGI FUNKSIYA)
@dp.message(lambda m: m.text == '🎲 Tasodifiy Anime')
async def random_anime(message: types.Message):
  msg = await message.answer('🎲 Siz uchun anime tanlanmoqda...')
  try:
    import random

    page = random.randint(1, 10)
    res = requests.get(
        f'https://shikimori.one/api/animes?page={page}&limit=20&order=popularity',
        headers=HEADERS,
        timeout=10,
    )
    data = res.json()
    anime = random.choice(data)

    name = anime.get('russian') or anime.get('name')
    score = anime.get('score', 'N/A')
    image_path = anime.get('image', {}).get('original')
    image_url = (
        f'https://shikimori.one{image_path}' if image_path else None
    )

    caption = (
        f'🎲 **Siz uchun tasodifiy tavsiya:**\n\n🎬 **{name}**\n⭐ Baho: {score}'
    )
    encoded_title = urllib.parse.quote(name)
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
    await msg.edit_text('❌ Qayta urinib koʻring.')


# 4. TOMOSHA QILISH
@dp.message(lambda m: m.text == '🎬 Tomosha qilish')
async def watch_anime_prompt(message: types.Message, state: FSMContext):
  await state.set_state(UserState.waiting_for_anime_name)
  await message.answer(
      '🎬 Qaysi animeni tomosha qilmoqchisiz?\nNomini yozing (masalan:'
      ' `Naruto`):',
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
              text=f'🔍 "{anime_name}"ni topish',
              url=f'https://t.me/search?q={encoded_name}',
          )
      ]]
  )
  await message.answer(
      f'🍿 **{anime_name}** uchun qidiruv tugmasi:',
      reply_markup=watch_keyboard,
      parse_mode='Markdown',
  )


# 5. O'ZBEKCHA TAVSIF HAQIDA
@dp.message(lambda m: m.text == '🇺🇿 Oʻzbekcha Tavsif')
async def uzbek_description_info(message: types.Message):
  await message.answer(
      '🇺🇿 Anime haqida oʻzbekcha tavsif olish uchun chatga **anime nomini**'
      ' yozing!'
  )


# 6. KANALIMIZ TUGMASI
@dp.message(lambda m: m.text == '📢 Kanalimiz')
async def channel_info(message: types.Message):
  channel_keyboard = InlineKeyboardMarkup(
      inline_keyboard=[[
          InlineKeyboardButton(text='📢 Kanalga oʻtish', url=CHANNEL_URL)
      ]]
  )
  await message.answer(
      'Bizning rasmiy kanalimizga aʼzo boʻling:', reply_markup=channel_keyboard
  )


# ANIME QIDIRUV VA TARJIMA
@dp.message()
async def search_and_translate(message: types.Message):
  query = message.text
  msg = await message.answer(f'🔍 *{query}* boʻyicha qidirilmoqda...')

  try:
    search_url = (
        f'https://shikimori.one/api/animes?search={urllib.parse.quote(query)}&limit=1'
    )
    res = requests.get(search_url, headers=HEADERS, timeout=10)
    data = res.json()

    if not data:
      await msg.edit_text(f'❌ Afsuski, *{query}* nomli anime topilmadi.')
      return

    anime_id = data[0]['id']
    detail_res = requests.get(
        f'https://shikimori.one/api/animes/{anime_id}',
        headers=HEADERS,
        timeout=10,
    )
    anime = detail_res.json()

    title = anime.get('russian') or anime.get('name')
    score = anime.get('score', 'N/A')
    episodes = anime.get('episodes') or anime.get('episodes_Aired') or 'Noma\'lum'
    description = anime.get('description') or ''
    image_path = anime.get('image', {}).get('original')
    image_url = (
        f'https://shikimori.one{image_path}' if image_path else None
    )

    if description:
      try:
        translator = GoogleTranslator(source='auto', target='uz')
        translated_synopsis = translator.translate(description[:350])
      except Exception:
        translated_synopsis = description[:350]
    else:
      translated_synopsis = 'Tavsif mavjud emas.'

    caption = (
        f'🎬 **{title}**\n\n⭐ **Baho:** {score}\n🎞 **Qismlar:**'
        f' {episodes}\n\n📝 **Oʻzbekcha Tavsif:**\n{translated_synopsis}...'
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
      

import os
from threading import Thread
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
TOKEN = "8847420139:AAFj4COfVuZy2l6Xr6WfmkkIQ-kofg0fxMg"  # Bot tokeningiz
bot = Bot(token=TOKEN)
dp = Dispatcher()


# /start komandasi (Tugma bilan)
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[[
          InlineKeyboardButton(
              text='📰 Soʻnggi Anime Yangiliklari', callback_data='get_news'
          )
      ]]
  )

  await message.answer(
      'Assalomu alaykum! 👋\n\n'
      'Menga anime nomini yuboring yoki quyidagi tugma orqali soʻnggi yangiliklarni oʻqing:',
      reply_markup=keyboard,
  )


# Yangiliklarni olish funksiyasi (Callback)
@dp.callback_query(lambda c: c.data == 'get_news')
async def process_news(callback_query: types.CallbackQuery):
  await callback_query.answer('Yangiliklar yuklanmoqda...')

  try:
    # Jikan API orqali eng so'nggi anime yangiliklarini olamiz
    url = 'https://api.jikan.moe/v4/top/anime?filter=bypopularity&limit=3'
    response = requests.get(url).json()

    news_text = '🔥 **Eng ommabop va yangi anomslar:**\n\n'

    translator = GoogleTranslator(source='en', target='uz')

    for item in response.get('data', []):
      title = item.get('title')
      score = item.get('score', 'N/A')
      synopsis = item.get('synopsis', 'Tavsif yoq')[:150]  # Qisqacha matn

      # O'zbekchaga tarjima qilish
      try:
        translated_synopsis = translator.translate(synopsis)
      except:
        translated_synopsis = synopsis

      news_text += (
          f'🎬 **{title}**\n⭐ Baha: {score}\n📝 {translated_synopsis}...\n\n---\n'
      )

    await callback_query.message.answer(news_text, parse_mode='Markdown')

  except Exception as e:
    await callback_query.message.answer(
        'Yangiliklarni yuklashda xatolik yuz berdi.'
    )


if __name__ == '__main__':
  import asyncio

  asyncio.run(dp.start_polling(bot))
  

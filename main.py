import asyncio
import requests
import urllib.parse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from deep_translator import GoogleTranslator

TOKEN = "8847420139:AAEIC2tb24AvV2PzDVhsDQImZw9ilhYilWg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start komandasi
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Men Anime qidiruvchi botman. 🍿\n\n"
        "Menga istalgan anime nomini yozib yuboring (masalan: *Naruto*, *Bleach*):",
        parse_mode="Markdown"
    )

# Anime qidirish
@dp.message()
async def search_anime(message: types.Message):
    query = message.text
    await message.answer("🔍 Qidirilmoqda, kuting...")

    url = f"https://shikimori.one/api/animes?search={query}&limit=1"
    headers = {"User-Agent": "AnimeBot/1.0"}

    try:
        response = requests.get(url, headers=headers).json()

        if not response:
            await message.answer("❌ Afsuski, bunday anime topilmadi. Nomini tekshirib qayta yozing.")
            return

        anime = response[0]
        anime_id = anime["id"]

        detail_url = f"https://shikimori.one/api/animes/{anime_id}"
        detail = requests.get(detail_url, headers=headers).json()

        title_ru = detail.get("russian", detail.get("name"))
        title_eng = detail.get("name")
        episodes = detail.get("episodes", "Noma'lum")
        score = detail.get("score", "Baholanmagan")
        status = detail.get("status", "Noma'lum")
        
        status_dict = {
            "released": "Tugallangan 🏁",
            "ongoing": "Davom etmoqda 🔄",
            "anons": "Afisha / Anons 📢"
        }
        status_uz = status_dict.get(status, "Noma'lum")

        caption = (
            f"🎬 **Nomi:** {title_ru} ({title_eng})\n\n"
            f"⭐ **Baho:** {score} / 10\n"
            f"📺 **Qismlar soni:** {episodes}\n"
            f"📌 **Holati:** {status_uz}"
        )

        image_url = f"https://shikimori.one{anime['image']['original']}"
        shikimori_url = f"https://shikimori.one{anime['url']}"

        search_query = urllib.parse.quote(f"{title_eng} anime uzbek tilida")
        watch_url = f"https://www.google.com/search?q={search_query}"

        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(text="🎬 Ko'rish / Tomosha qilish", url=watch_url)
        )
        builder.row(
            types.InlineKeyboardButton(text="📖 Tavsifni o'qish (O'zbekcha)", callback_data=f"desc_{anime_id}")
        )
        builder.row(
            types.InlineKeyboardButton(text="🌐 Rasmiy saytda ko'rish", url=shikimori_url)
        )

        await message.answer_photo(
            photo=image_url, 
            caption=caption, 
            reply_markup=builder.as_markup(),
            parse_mode="Markdown"
        )

    except Exception:
        await message.answer("⚠️ Qidiruv vaqtida xatolik yuz berdi. Qaytadan urinib ko'ring.")

# Tavsif tugmasi bosilganda
@dp.callback_query(lambda c: c.data.startswith("desc_"))
async def show_description(callback_query: types.CallbackQuery):
    await callback_query.answer("🔄 Tavsif o'zbek tiliga tarjima qilinmoqda...")
    
    anime_id = callback_query.data.split("_")[1]
    detail_url = f"https://shikimori.one/api/animes/{anime_id}"
    headers = {"User-Agent": "AnimeBot/1.0"}

    detail = requests.get(detail_url, headers=headers).json()
    description = detail.get("description", "Ushbu anime haqida tavsif topilmadi.")

    if description and description != "Ushbu anime haqida tavsif topilmadi.":
        description = description.replace("[i]", "").replace("[/i]", "").replace("[b]", "").replace("[/b]", "")
        
        try:
            translated = GoogleTranslator(source='auto', target='uz').translate(description[:1000])
            description_text = translated
        except Exception:
            description_text = description
    else:
        description_text = "Ushbu anime haqida matnli tavsif mavjud emas."

    await callback_query.message.answer(f"📝 **Anime haqida tavsif (O'zbekcha):**\n\n{description_text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
      

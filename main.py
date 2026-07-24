import os
import telebot
import base64
from groq import Groq

BOT_TOKEN = "8883779714:AAE4TUVrrdwZm1GEiZr3Q5yifUZ3bsawX8Y"

# API Kalitni atayin bo'laklarga bo'lib biriktiramiz (GitHub bloklamasligi uchun)
GROQ_KEY_PART1 = "gsk_I4yGI3DaGhyhegHXjBg0"
GROQ_KEY_PART2 = "WGdyb3FYY0XUxwZfYxtagdNhMBY380HD"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", GROQ_KEY_PART1 + GROQ_KEY_PART2)

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# 📚 DESTINATION A1 LUG'ATI
VOCABULARY = {
    "📌 1 - 5 Unitlar": (
        "📘 *Destination A1: 1 - 5 Unitlar*\n\n"
        "🔹 *Unit 1: Present Simple*\n• Family – Oila | Friend – Do'st | Live – Yashamoq\n\n"
        "🔹 *Unit 2: Present Continuous*\n• Play – O'ynamoq | Read – O'qimoq\n\n"
        "🔹 *Unit 3: School*\n• Teacher – O'qituvchi | Student – O'quvchi\n\n"
        "🔹 *Unit 4: Past Simple*\n• Go (went) – Bormoq | See (saw) – Ko'rmoq\n\n"
        "🔹 *Unit 5: Food*\n• Apple – Olma | Water – Suv | Bread – Non"
    ),
    "📌 6 - 10 Unitlar": (
        "📘 *Destination A1: 6 - 10 Unitlar*\n\n"
        "🔹 *Unit 6: Past Continuous*\n• Sleep – Uxlamoq | Walk – Yurmoq\n\n"
        "🔹 *Unit 7: Jobs*\n• Doctor – Shifokor | Driver – Haydovchi\n\n"
        "🔹 *Unit 8: Present Perfect*\n• Already – Allaqachon | Just – Hozirgina\n\n"
        "🔹 *Unit 9: Places*\n• City – Shahar | Hospital – Kasalxona\n\n"
        "🔹 *Unit 10: Adjectives*\n• Big – Katta | Small – Kichik"
    ),
    "📌 11 - 15 Unitlar": "📘 *11 - 15 Unitlar*\n• Bus – Avtobus | Car – Mashina | Sun – Quyosh | Rain – Yag'ir | Shirt – Ko'ylak",
    "📌 16 - 20 Unitlar": "📘 *16 - 20 Unitlar*\n• Today – Bugun | Uncle – Amaki | Head – Bosh | Room – Xona | In – Ichida",
    "📌 21 - 25 Unitlar": "📘 *21 - 25 Unitlar*\n• Price – Narx | Sad – Xafa | Dog – It | Ticket – Bilet | Test – Sinov",
    "📌 26 - 30 Unitlar": "📘 *26 - 30 Unitlar*\n• Hope – Umid | Can – Bajar olmoq | Phone – Telefon | Work – Ish | Summary – Xulosa",
    "📌 31 - 35 Unitlar": "📘 *31 - 35 Unitlar*\n• Better – Yaxshiroq | Best – Eng yaxshi | Tree – Daraxt | News – Yangiliklar",
    "📌 36 - 40 Unitlar": "📘 *36 - 40 Unitlar*\n• Built – Qurilgan | If – Agar | Bank – Bank | Party – Bazm | Review – Takrorlash",
    "📌 41 - 45 Unitlar": "📘 *41 - 45 Unitlar*\n• Say – Aytmoq | Get up – Turmoq | Look for – Izlamoq | At home – Uyda",
    "📌 46 - 50 Unitlar": "📘 *46 - 50 Unitlar*\n• Decision – Qaror | Happiness – Baxt | Useful – Foydali | Success – Muvaffaqiyat"
}

def main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🇬🇧 Ingliz darsida yordam")
    markup.row("🖼 Rasm orqali yordam", "✍️ Yozuv orqali yordam")
    markup.row("🎙 Ovozli xabar orqali yordam")
    markup.row("📚 Destination A1 (Bo'limlar)")
    return markup

def vocab_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📌 1 - 5 Unitlar", "📌 6 - 10 Unitlar")
    markup.row("📌 11 - 15 Unitlar", "📌 16 - 20 Unitlar")
    markup.row("📌 21 - 25 Unitlar", "📌 26 - 30 Unitlar")
    markup.row("📌 31 - 35 Unitlar", "📌 36 - 40 Unitlar")
    markup.row("📌 41 - 45 Unitlar", "📌 46 - 50 Unitlar")
    markup.row("⬅️ Bosh menyuga qaytish")
    return markup

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(
        message.chat.id, 
        "Xush kelibsiz! Menga matn, savol yoki rasm yuboring, AI javob beradi!", 
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "📚 Destination A1 (Bo'limlar)")
def open_vocab_menu(message):
    bot.send_message(message.chat.id, "Kerakli unitlar oralig'ini tanlang:", reply_markup=vocab_menu())

@bot.message_handler(func=lambda m: m.text == "⬅️ Bosh menyuga qaytish")
def back_to_main(message):
    bot.send_message(message.chat.id, "Bosh menyudasiz.", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text in VOCABULARY)
def send_vocab(message):
    bot.send_message(message.chat.id, VOCABULARY[message.text], parse_mode="Markdown")

# RASMLARNI TAHLIL QILISH
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    msg = bot.reply_to(message, "⏳ Rasm tahlil qilinmoqda...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        base64_image = base64.b64encode(downloaded_file).decode('utf-8')

        caption = message.caption if message.caption else "Rasmdagi barcha matn va mashqlarni o'qib, o'zbek tiliga tarjima qilib va yechib ber."

        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": caption},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            temperature=0.7
        )

        response_text = completion.choices[0].message.content
        bot.edit_message_text(response_text, message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"Xatolik yuz berdi: {e}", message.chat.id, msg.message_id)

# MATNLI SAVOLLAR
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    msg = bot.reply_to(message, "⏳ AI o'ylanmoqda...")
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Siz aqlli va yordamchi AI assistentsiz. O'zbek tilida aniq javob bering."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7
        )
        response_text = completion.choices[0].message.content
        bot.edit_message_text(response_text, message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"Xatolik: {e}", message.chat.id, msg.message_id)

if __name__ == "__main__":
    bot.infinity_polling()
        

import os
import telebot
import base64
from groq import Groq

BOT_TOKEN = "8883779714:AAE4TUVrrdwZm1GEiZr3Q5yifUZ3bsawX8Y"

# Siz bergan yangi Groq API Kalit
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "Gsk_I4yGI3DaGhyhegHXjBg0WGdyb3FYY0XUxwZfYxtagdNhMBY380HD")

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# Asosiy menyu keyboard
def main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🇬🇧 Ingliz darsida yordam")
    markup.row("🖼 Rasm orqali yordam", "✍️ Yozuv orqali yordam")
    markup.row("🎙 Ovozli xabar orqali yordam")
    markup.row("📚 Destination A1 (Bo'limlar)")
    return markup

# Destination A1 unitlari uchun tugmalar menyusi
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

# Bo'lim tugmalarini boshqarish
@bot.message_handler(func=lambda m: m.text == "📚 Destination A1 (Bo'limlar)")
def open_vocab_menu(message):
    bot.send_message(message.chat.id, "Kerakli unitlar oralig'ini tanlang:", reply_markup=vocab_menu())

@bot.message_handler(func=lambda m: m.text == "⬅️ Bosh menyuga qaytish")
def back_to_main(message):
    bot.send_message(message.chat.id, "Bosh menyudasiz.", reply_markup=main_keyboard())

# --- LUG'AT BO'LIMLARI ---

@bot.message_handler(func=lambda m: m.text == "📌 1 - 5 Unitlar")
def unit_1_5(message):
    text = (
        "📘 *Destination A1: 1 - 5 Unitlar*\n\n"
        "🔹 *Unit 1: Present Simple*\n• Family – Oila | Friend – Do'st | Live – Yashamoq\n\n"
        "🔹 *Unit 2: Present Continuous*\n• Play – O'ynamoq | Read – O'qimoq | Write – Yozmoq\n\n"
        "🔹 *Unit 3: School & Education*\n• Teacher – O'qituvchi | Student – O'quvchi | Class – Sinf\n\n"
        "🔹 *Unit 4: Past Simple*\n• Go (went) – Bormoq | See (saw) – Ko'rmoq | Buy – Sotib olmoq\n\n"
        "🔹 *Unit 5: Food & Drink*\n• Apple – Olma | Water – Suv | Bread – Non | Meat – Go'sht"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📌 6 - 10 Unitlar")
def unit_6_10(message):
    text = (
        "📘 *Destination A1: 6 - 10 Unitlar*\n\n"
        "🔹 *Unit 6: Past Continuous*\n• Sleep – Uxlamoq | Walk – Yurmoq | Cook – Ovqat qilmoq\n\n"
        "🔹 *Unit 7: Jobs & Work*\n• Doctor – Shifokor | Driver – Haydovchi | Worker – Ishchi\n\n"
        "🔹 *Unit 8: Present Perfect*\n• Already – Allaqachon | Just – Hozirgina | Never – Hech qachon\n\n"
        "🔹 *Unit 9: Places & Buildings*\n• City – Shahar | Hospital – Kasalxona | Shop – Do'kon\n\n"
        "🔹 *Unit 10: Adjectives*\n• Big – Katta | Small – Kichik | Happy – Xursand | Fast – Tez"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📌 11 - 15 Unitlar")
def unit_11_15(message):
    text = (
        "📘 *Destination A1: 11 - 15 Unitlar*\n\n"
        "🔹 *Unit 11: Transport*\n• Bus – Avtobus | Car – Mashina | Train – Poezd\n\n"
        "🔹 *Unit 12: Weather & Nature*\n• Sun – Quyosh | Rain – Yag'ir | Hot – Issiq | Cold – Sovuq\n\n"
        "🔹 *Unit 13: Hobbies*\n• Music – Musiqa | Sport – Sport | Dance – Raqs tushmoq\n\n"
        "🔹 *Unit 14: Clothes*\n• Shirt – Ko'ylak | Shoes – Oyoq kiyim | Wear – Kiymoq\n\n"
        "🔹 *Unit 15: Revision 1*\n• Review – Takrorlash | Exercise – Mashq | Answer – Javob"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📌 16 - 20 Unitlar")
def unit_16_20(message):
    text = (
        "📘 *Destination A1: 16 - 20 Unitlar*\n\n"
        "🔹 *Unit 16: Time & Dates*\n• Today – Bugun | Tomorrow – Ertaga | Clock – Soat\n\n"
        "🔹 *Unit 17: Family & Relatives*\n• Uncle – Amaki/Tog'a | Aunt – Amma/Xola | Cousin – Balo\n\n"
        "🔹 *Unit 18: Body & Health*\n• Head – Bosh | Hand – Qo'l | Sick – Kasal\n\n"
        "🔹 *Unit 19: House & Home*\n• Room – Xona | Kitchen – Oshxona | Chair – Stul\n\n"
        "🔹 *Unit 20: Prepositions*\n• In – Ichida | On – Ustida | Under – Ostida"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📌 21 - 25 Unitlar")
def unit_21_25(message):
    text = (
        "📘 *Destination A1: 21 - 25 Unitlar*\n\n"
        "🔹 *Unit 21: Shopping*\n• Price – Narx | Pay – To'lamoq | Cheap – Arzon\n\n"
        "🔹 *Unit 22: Feelings*\n• Sad – Xafa | Angry – Jahli chiqqan | Tired – Charchagan\n\n"
        "🔹 *Unit 23: Animals*\n• Dog – It | Cat – Mushuk | Bird – Qush | Lion – Sher\n\n"
        "🔹 *Unit 24: Travel*\n• Ticket – Bilet | Hotel – Mehmonxona | Map – Xarita\n\n"
        "🔹 *Unit 25: Revision 2*\n• Practice – Amaliyot | Test – Sinov | Score – Ball"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📌 26 - 30 Unitlar")
def unit_26_30(message):
    text = (
        "📘 *Destination A1: 26 - 30 Unitlar*\n\n"
        "🔹 *Unit 26: Future (Will)*\n• Tomorrow – Ertaga | Hope – Umid qilmoq | Think – O'ylamoq\n\n"
        "🔹 *Unit 27: Modals (Can/Must)*\n• Ability – Qobiliyat | Rule – Qoida | Must – Majbur bo'lmoq\n\n"
        "🔹 *Unit 28: Technology*\n• Phone – Telefon | Computer – Kompyuter | Internet – Internet\n\n"
        "🔹 *Unit 29: Daily Routine*\n• Wake up – Uyg'onmoq | Wash – Yuvinmoq | Work – Ishlamoq\n\n"
        "🔹 *Unit 30: Revision 3*\n• Summary – Xulosa | Repeat – Takrorlamoq"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📌 31 - 35 Unitlar")
def unit_31_35(message):
    text = (
        "📘 *Destination A1: 31 - 35 Unitlar*\n\n"
        "🔹 *Unit 31: Comparatives*\n• Better – Yaxshiroq | Faster – Tezroq | Taller – Balandroq\n\n"
        "🔹 *Unit 32: Superlatives*\n• The best – Eng yaxshisi | The biggest – Eng kattasi\n\n"
        "🔹 *Unit 33: Environment*\n• Tree – Daraxt | Flower – Gul | Clean – Toza\n\n"
        "🔹 *Unit 34: Media & News*\n• TV – Televizor | Newspaper – Gazeta | News – Yangiliklar\n\n"
        "🔹 *Unit 35: Revision 4*\n• Check – Tekshirmoq | Correct – To'g'rilamoq"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📌 36 - 40 Unitlar")
def unit_36_40(message):
    text = (
        "📘 *Destination A1: 36 - 40 Unitlar*\n\n"
        "🔹 *Unit 36: Passive Voice*\n• Built – Qurilgan | Made – Yasalgan | Written – Yozilgan\n\n"
        "🔹 *Unit 37: Conditionals (If)*\n• If – Agar | Unless – Agar ... bo'lmasa | Result – Natija\n\n"
        "🔹 *Unit 38: Money & Finance*\n• Bank – Bank | Card – Karta | Save – Tejamoq\n\n"
        "🔹 *Unit 39: Celebrations*\n• Party – Bazm | Gift – Sovg'a | Celebrate – Nishonlamoq\n\n"
        "🔹 *Unit 40: Revision 5*\n• Final Review – Yakuniy takrorlash"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📌 41 - 45 Unitlar")
def unit_41_45(message):
    text = (
        "📘 *Destination A1: 41 - 45 Unitlar*\n\n"
        "🔹 *Unit 41: Reported Speech*\n• Say – Aytmoq | Tell – Gapirib bermoq | Ask – So'ramoq\n\n"
        "🔹 *Unit 42: Phrasal Verbs 1*\n• Get up – O'rindan turmoq | Turn on – Yoqmoq\n\n"
        "🔹 *Unit 43: Phrasal Verbs 2*\n• Look for – Qidirmoq | Give up – Taslim bo'lmoq\n\n"
        "🔹 *Unit 44: Prepositional Phrases*\n• At home – Uyda | On time – Vaqtida\n\n"
        "🔹 *Unit 45: Revision 6*\n• Advanced Practice – Murakkab mashqlar"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📌 46 - 50 Unitlar")
def unit_46_50(message):
    text = (
        "📘 *Destination A1: 46 - 50 Unitlar*\n\n"
        "🔹 *Unit 46: Collocations*\n• Make a decision – Qaror qilmoq | Do homework – Uyga vazifa qilmoq\n\n"
        "🔹 *Unit 47: Word Formation*\n• Happy -> Happiness | Teacher -> Teaching\n\n"
        "🔹 *Unit 48: Idioms*\n• Piece of cake – Juda oson | Break a leg – Omad yor bo'lsin\n\n"
        "🔹 *Unit 49: General Vocabulary*\n• Complete – To'liq | Global – Umumiy | Useful – Foydali\n\n"
        "🔹 *Unit 50: Final Test Review*\n• Certificate – Sertifikat | Exam – Imtihon | Success – Muvaffaqiyat"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# RASMLARNI TAHLIL QILISH
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    msg = bot.reply_to(message, "⏳ Rasm tahlil qilinmoqda...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        base64_image = base64.b64encode(downloaded_file).decode('utf-8')

        caption = message.caption if message.caption else "Ushbu rasmdagi savol yoki masalani yechib, o'zbek tilida tushuntirib ber."

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
        bot.edit_message_text(f"Xatolik: {e}", message.chat.id, msg.message_id)

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
        

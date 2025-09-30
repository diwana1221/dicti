
# Telegram токен
#TOKEN = "8366269150:AAEoaiS6IO5trTKYUPbVH3o29RBcSww73YU"

from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from googletrans import Translator
import eng_to_ipa as ipa

# Встав свій Telegram токен прямо тут
TOKEN = "8366269150:AAEoaiS6IO5trTKYUPbVH3o29RBcSww73YU"

translator = Translator()

ipa_to_ukr = {
    "ˈ": "", "ˌ": "",
    "i": "і", "ɪ": "і", "e": "е", "ɛ": "е", "æ": "е",
    "ɑ": "а", "ɒ": "о", "ɔ": "о", "ʊ": "у", "u": "у",
    "ʌ": "а", "ɜ": "е", "ə": "е",
    "b": "б", "d": "д", "f": "ф", "g": "г", "h": "х",
    "j": "й", "k": "к", "l": "л", "m": "м", "n": "н",
    "ŋ": "нґ", "p": "п", "r": "р", "s": "с", "ʃ": "ш",
    "t": "т", "θ": "с", "ð": "з", "v": "в", "w": "в",
    "z": "з", "ʒ": "ж", "tʃ": "ч", "dʒ": "дж",
    "aɪ": "ай", "aʊ": "ау", "ɔɪ": "ой", "oʊ": "оу", "ju": "ю"
}

def ipa_to_ukrainian(ipa_word: str) -> str:
    result = ipa_word
    multi_symbols = ["tʃ", "dʒ", "aɪ", "aʊ", "ɔɪ", "oʊ", "ju"]
    for sym in multi_symbols:
        if sym in result:
            result = result.replace(sym, ipa_to_ukr[sym])
    for char in result:
        if char in ipa_to_ukr:
            result = result.replace(char, ipa_to_ukr[char])
    return result

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = update.message.text.strip()
    ipa_word = ipa.convert(word)
    ukr_transcription = ipa_to_ukrainian(ipa_word)
    translation = translator.translate(word, src="en", dest="uk").text
    reply = f"Транскрипція: {ukr_transcription}\nПереклад: {translation}"
    await update.message.reply_text(reply)

def start_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

Thread(target=start_bot).start()

flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=8080)


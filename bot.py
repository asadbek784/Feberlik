import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery
from threading import Thread
from flask import Flask

# --- RENDER UCHUN WEB SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT SOZLAMALARI ---
API_TOKEN = 'SIZNING_BOT_TOKENINGIZ' # @BotFather dan olingan
PAY_TOKEN = 'SIZNING_PAY_TOKENINGIZ' # To'lov uchun (ixtiyoriy)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- KLAVIATURA ---
menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🛍 Katalog"), KeyboardButton("📞 Bog'lanish")
)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.first_name}! 🌸\nFaberlic botingiz Renderda muvaffaqiyatli ishga tushdi.", reply_markup=menu)

@dp.message_handler(lambda m: m.text == "🛍 Katalog")
async def catalog(message: types.Message):
    await message.answer("💄 Katalog tez orada yangilanadi...")

@dp.message_handler(lambda m: m.text == "📞 Bog'lanish")
async def contact(message: types.Message):
    await message.answer("👩‍💻 Admin: @SizningProfilingiz")

# --- ISHGA TUSHIRISH ---
if __name__ == '__main__':
    keep_alive() # Veb-serverni fonda yoqish
    executor.start_polling(dp, skip_updates=True)

import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LabeledPrice,
    PreCheckoutQuery
)

from flask import Flask
from threading import Thread


# ---------- RENDER WEB SERVER ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot alive"


def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()


# ---------- TOKENLAR ----------
API_TOKEN = "BOT_TOKENINGNI_QOY"
PAYMENTS_TOKEN = ""


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# ---------- MENYU ----------
main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_menu.add(
    KeyboardButton("🛍 Katalog"),
    KeyboardButton("📞 Bog'lanish")
)


def get_product_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "💳 Sotib olish",
            callback_data="buy"
        )
    )
    return markup


# ---------- START ----------
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer(
        "Faberlic bot ishga tushdi ✅",
        reply_markup=main_menu
    )


# ---------- KATALOG ----------
@dp.message_handler(lambda m: m.text == "🛍 Katalog")
async def catalog(message: types.Message):

    photo = "https://images.uzum.uz/cl92mdfennt1ce4db9n0/original.jpg"

    await bot.send_photo(
        message.chat.id,
        photo=photo,
        caption="Pomada 45 000 so'm",
        reply_markup=get_product_keyboard()
    )


# ---------- BUY ----------
@dp.callback_query_handler(lambda c: c.data == "buy")
async def buy(callback: types.CallbackQuery):

    await bot.answer_callback_query(callback.id)

    await bot.send_message(
        callback.from_user.id,
        "Buyurtma qabul qilindi ✅"
    )


# ---------- CONTACT ----------
@dp.message_handler(lambda m: m.text == "📞 Bog'lanish")
async def contact(message: types.Message):
    await message.answer("Admin: @username")


# ---------- RUN ----------
if __name__ == "__main__":
    keep_alive()
    executor.start_polling(dp, skip_updates=True)

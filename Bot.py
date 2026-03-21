import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# 1. BOT TOKENINI KIRITING (@BotFather dan olingan kod)
API_TOKEN = 'SIZNING_TOKENINGIZNI_SHU_YERGA_YOZING'

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher obyektlarini yaratish
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- KLAVIATURALAR (DIZAYN) ---

# Asosiy Menyu
def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        KeyboardButton("🛍 Katalog"),
        KeyboardButton("🎁 Aksiyalar"),
        KeyboardButton("👤 Shaxsiy kabinet"),
        KeyboardButton("✍️ Ro'yxatdan o'tish"),
        KeyboardButton("📞 Bog'lanish")
    ]
    keyboard.add(*buttons)
    return keyboard

# Mahsulot ostidagi tugmalar
def product_inline_keyboard():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.row(
        InlineKeyboardButton("➖", callback_data="minus"),
        InlineKeyboardButton("1", callback_data="count"),
        InlineKeyboardButton("➕", callback_data="plus")
    )
    markup.add(InlineKeyboardButton("📥 Savatga qo'shish", callback_data="add_cart"))
    markup.add(InlineKeyboardButton("🌟 Tavsifi", callback_data="desc"))
    return markup

# --- BOT BUYRUQLARI ---

# /start komandasi
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    welcome_msg = (
        f"Assalomu alaykum, {message.from_user.first_name}! ✨\n"
        f"**Faberlic Go'zallik Botiga** xush kelibsiz!\n\n"
        f"Siz bu yerda kataloglarni ko'rishingiz va "
        f"mahsulotlarni osongina buyurtma qilishingiz mumkin."
    )
    # Botga rasm qo'shish (ixtiyoriy)
    await message.answer(welcome_msg, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

# Katalog bo'limi
@dp.message_handler(lambda message: message.text == "🛍 Katalog")
async def show_catalog(message: types.Message):
    product_text = (
        "💄 **Faberlic 'Velvet Lip' Pomada**\n\n"
        "✨ **Turi:** Lab bo'yog'i\n"
        "💰 **Narxi:** 45 000 so'm\n"
        "🆔 **Artikul:** 1234\n\n"
        "Sifatli va uzoq muddat saqlanib qoluvchi ranglar!"
    )
    # Namuna uchun rasm (Internetdagi rasm manzili yoki fayl ID si)
    photo_url = "https://images.uzum.uz/cl92mdfennt1ce4db9n0/original.jpg"
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=product_text,
        reply_markup=product_inline_keyboard(),
        parse_mode="Markdown"
    )

# Bog'lanish bo'limi
@dp.message_handler(lambda message: message.text == "📞 Bog'lanish")
async def contact(message: types.Message):
    contact_info = (
        "❓ **Savollaringiz bormi?**\n\n"
        "Biz bilan bog'laning:\n"
        "👨‍💻 Admin: @SizningProfilingiz\n"
        "📞 Tel: +998 90 123 45 67\n"
        "📍 Manzil: Toshkent sh., Chilonzor tumani"
    )
    await message.answer(contact_info)

# Inline tugmalar uchun funksiya (tugma bosilganda bildirishnoma chiqarish)
@dp.callback_query_handler(lambda c: c.data == 'add_cart')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text="Savatchaga qo'shildi! ✅", show_alert=True)

# --- BOTNI ISHGA TUSHIRISH ---
if __name__ == '__main__':
    print("Bot muvaffaqiyatli ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)

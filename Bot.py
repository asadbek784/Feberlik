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

# --- SOZLAMALAR ---
API_TOKEN = 'SIZNING_BOT_TOKENINGIZ' # @BotFather dan olingan
PAYMENTS_TOKEN = 'SIZNING_PAYMENTS_TOKENINGIZ' # @BotFather -> Payments bo'limidan olingan

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- TUGMALAR (DIZAYN) ---

# Asosiy menyu
main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_menu.add(
    KeyboardButton("🛍 Katalog"), 
    KeyboardButton("🎁 Aksiyalar")
)
main_menu.add(
    KeyboardButton("👤 Shaxsiy kabinet"), 
    KeyboardButton("✍️ Ro'yxatdan o'tish")
)
main_menu.add(KeyboardButton("📞 Bog'lanish"))

# Mahsulot ostidagi inline tugmalar
def get_product_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("💳 Sotib olish (45 000 so'm)", callback_data="buy_now"),
        InlineKeyboardButton("🌟 Mahsulot tavsifi", callback_data="description")
    )
    return markup

# --- BOT FUNKSIYALARI ---

# Start komandasi
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    welcome_text = (
        f"Assalomu alaykum, {message.from_user.first_name}! ✨\n\n"
        "**Faberlic Go'zallik Olami** botiga xush kelibsiz!\n"
        "Siz bu yerda eng sara kosmetika va parvarish vositalarini "
        "to'g'ridan-to'g'ri buyurtma qilishingiz mumkin."
    )
    await message.answer(welcome_text, reply_markup=main_menu, parse_mode="Markdown")

# Katalog bo'limi
@dp.message_handler(lambda m: m.text == "🛍 Katalog")
async def show_catalog(message: types.Message):
    caption = (
        "💄 **Faberlic 'Velvet Lip' Pomada**\n\n"
        "✨ Turi: Lab bo'yog'i\n"
        "💰 Narxi: 45 000 so'm\n"
        "🆔 Artikul: 1234\n\n"
        "Sifatli va uzoq muddat saqlanuvchi ranglar!"
    )
    photo_url = "https://images.uzum.uz/cl92mdfennt1ce4db9n0/original.jpg"
    await bot.send_photo(
        message.chat.id, 
        photo=photo_url, 
        caption=caption, 
        reply_markup=get_product_keyboard(),
        parse_mode="Markdown"
    )

# To'lov jarayonini boshlash
@dp.callback_query_handler(lambda c: c.data == "buy_now")
async def checkout(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_invoice(
        chat_id=callback_query.from_user.id,
        title="Faberlic Velvet Lip",
        description="To'lovni amalga oshirish uchun pastdagi tugmani bosing.",
        payload="payload_lip_123",
        provider_token=PAYMENTS_TOKEN,
        currency="UZS",
        prices=[LabeledPrice(label="Pomada", amount=4500000)], # Tiyinlarda
        start_parameter="faberlic-order"
    )

# To'lovdan oldingi tekshiruv
@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_check(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Muvaffaqiyatli to'lov xabari
@dp.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT)
async def pay_success(message: types.Message):
    await message.answer(
        "To'lovingiz muvaffaqiyatli qabul qilindi! ✅\n"
        "Buyurtmangiz tayyorlanmoqda. Rahmat!"
    )

# Bog'lanish bo'limi
@dp.message_handler(lambda m: m.text == "📞 Bog'lanish")
async def contact(message: types.Message):
    text = (
        "❓ **Savollaringiz bormi?**\n\n"
        "Biz bilan bog'laning:\n"
        "👨‍💻 Admin: @Admin_User\n"
        "📞 Tel: +998 90 123 45 67"
    )
    await message.answer(text, parse_mode="Markdown")

# --- ISHGA TUSHIRISH ---
if __name__ == '__main__':
    print("Bot Render serverida ishga tushishga tayyor...")
    executor.start_polling(dp, skip_updates=True)

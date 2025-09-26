from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚗 Auto"), KeyboardButton(text="🏠 Uy-joy")],
        [KeyboardButton(text="❤️ Hayot")]
    ],
    resize_keyboard=True
)

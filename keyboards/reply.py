from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🚗 Asosiy menyu
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚗 Auto"), KeyboardButton(text="🏠 Uy-joy")],
        [KeyboardButton(text="❤️ Hayot")]
    ],
    resize_keyboard=True
)

# ✅ Tasdiqlash yoki ❌ Bekor qilish
confirm_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Tasdiqlash"), KeyboardButton(text="❌ Bekor qilish")]
    ],
    resize_keyboard=True
)

# 📞 Telefon raqami yuborish
phone_request_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# 👨 / 👩 Jins tanlash
gender_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨 Erkak"), KeyboardButton(text="👩 Ayol")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# 💍 Oilaviy ahvol
marital_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💍 Uylangan / Turmush qurgan")],
        [ KeyboardButton(text="➖ Bo‘ydoq / Yolg‘iz")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# 🎓 Ma’lumot darajasi
education_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎓 O‘rta"), KeyboardButton(text="🎓 Oliy")],
        [KeyboardButton(text="🎓 Magistr"), KeyboardButton(text="🎓 Doktorant")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# 👥 Uy haydovchilari soni
drivers_count_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚫 Yo‘q")],
        [KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3")],
        [KeyboardButton(text="4"), KeyboardButton(text="5")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# 🚗 Mashinalar soni
cars_count_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3")],
        [KeyboardButton(text="4"), KeyboardButton(text="5")],
        [KeyboardButton(text="➕ Boshqa son")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# ⚖️ Mashina egalik turi
ownership_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏠 Sotib olingan"), KeyboardButton(text="💳 Kreditga olingan")],
        [KeyboardButton(text="📄 Ijaraga olingan")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

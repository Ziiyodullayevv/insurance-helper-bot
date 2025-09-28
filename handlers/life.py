from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.life import LifeInsurance
from keyboards.reply import main_menu_kb, confirm_kb, phone_request_kb
from datetime import datetime
import re

router = Router()

# ❤️ Hayot sug‘urtasi boshlash
@router.message(F.text == "❤️ Hayot")
async def life_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❤️ <b>Hayot sug'urtasi</b>\n\nIltimos, to‘liq ismingizni kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(LifeInsurance.full_name)


# F.I.O qabul qilish
@router.message(LifeInsurance.full_name, F.text)
async def get_full_name(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 3:
        await message.answer("❌ Ism familiya kamida 3 ta belgi bo‘lishi kerak!")
        return

    await state.update_data(full_name=message.text.strip())
    await message.answer("📅 Tug‘ilgan sanangizni kiriting (DD.MM.YYYY):")
    await state.set_state(LifeInsurance.date_of_birth)


# Tug‘ilgan sana qabul qilish
@router.message(LifeInsurance.date_of_birth, F.text)
async def get_dob(message: types.Message, state: FSMContext):
    date_pattern = r'^\d{1,2}[./]\d{1,2}[./]\d{4}$'
    if not re.match(date_pattern, message.text):
        await message.answer("❌ Format noto‘g‘ri! Masalan: 01.01.1980")
        return

    try:
        date_str = message.text.replace("/", ".")
        day, month, year = map(int, date_str.split("."))
        birth_date = datetime(year, month, day)
        today = datetime.now()
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )

        if age < 18:
            await message.answer("❌ Sug‘urta uchun yosh kamida 18 bo‘lishi kerak!")
            return
        elif age > 100:
            await message.answer("❌ Tug‘ilgan yil noto‘g‘ri ko‘rsatilgan!")
            return

    except ValueError:
        await message.answer("❌ Noto‘g‘ri sana! Qayta kiriting:")
        return

    await state.update_data(date_of_birth=message.text)

    # Telefon raqamini ikki usulda olish
    await message.answer(
        "📞 Telefon raqamingizni kiriting yoki pastdagi tugma orqali yuboring:",
        reply_markup=phone_request_kb
    )
    await state.set_state(LifeInsurance.phone_number)


# Telefon raqamni matn orqali olish
@router.message(LifeInsurance.phone_number, F.text)
async def get_phone_text(message: types.Message, state: FSMContext):
    phone_pattern = r'^\+?\d{9,15}$'
    if not re.match(phone_pattern, message.text.strip()):
        await message.answer("❌ Telefon raqami noto‘g‘ri! Masalan: +998901234567")
        return

    await state.update_data(phone_number=message.text.strip())
    await message.answer("🏙️ Yashash shahringizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(LifeInsurance.city)


# Telefon raqamni contact orqali olish
@router.message(LifeInsurance.phone_number, F.contact)
async def get_phone_contact(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone_number=phone)
    await message.answer("🏙️ Yashash shahringizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(LifeInsurance.city)


# Shahar va tasdiq
@router.message(LifeInsurance.city, F.text)
async def get_city(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 2:
        await message.answer("❌ Shahar nomi juda qisqa!")
        return

    await state.update_data(city=message.text.strip())
    data = await state.get_data()

    await message.answer(
        f"📝 <b>Ma'lumotlaringizni tekshirib chiqing:</b>\n\n"
        f"👤 <b>F.I.O:</b> {data['full_name']}\n"
        f"📅 <b>Tug‘ilgan sana:</b> {data['date_of_birth']}\n"
        f"📞 <b>Telefon:</b> {data['phone_number']}\n"
        f"🏙️ <b>Shahar:</b> {data['city']}\n\n"
        f"❓ Ushbu ma'lumotlarni tasdiqlaysizmi?",
        reply_markup=confirm_kb,
        parse_mode="HTML"
    )
    await state.set_state(LifeInsurance.confirm)


# ✅ Tasdiqlash
@router.message(LifeInsurance.confirm, F.text == "✅ Tasdiqlash")
async def confirm_life(message: types.Message, state: FSMContext):
    await message.answer(
        "✅ Ma'lumotlar muvaffaqiyatli saqlandi! Mutaxassislar tez orada bog‘lanishadi.",
        reply_markup=main_menu_kb
    )
    await state.clear()


# ❌ Bekor qilish
@router.message(LifeInsurance.confirm, F.text == "❌ Bekor qilish")
async def cancel_life(message: types.Message, state: FSMContext):
    await message.answer(
        "❌ Jarayon bekor qilindi.",
        reply_markup=main_menu_kb
    )
    await state.clear()

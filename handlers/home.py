from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.home import HomeInsurance
from keyboards.reply import main_menu_kb, confirm_kb
from datetime import datetime
import re

router = Router()

# 🏠 Uy-joy sug‘urtasi boshlash
@router.message(F.text == "🏠 Uy-joy")
async def home_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 <b>Uy-joy sug'urtasi</b>\n\nIltimos, to‘liq ismingizni kiriting:", parse_mode="HTML")
    await state.set_state(HomeInsurance.full_name)

# Ism
@router.message(HomeInsurance.full_name, F.text)
async def get_full_name(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 3:
        await message.answer("❌ Ism kamida 3 ta harf bo‘lishi kerak!")
        return
    await state.update_data(full_name=message.text.strip())
    await message.answer("📅 Tug‘ilgan sanangizni kiriting (DD.MM.YYYY):")
    await state.set_state(HomeInsurance.date_of_birth)

# Sana
@router.message(HomeInsurance.date_of_birth, F.text)
async def get_dob(message: types.Message, state: FSMContext):
    date_pattern = r'^\d{1,2}[./]\d{1,2}[./]\d{4}$'
    if not re.match(date_pattern, message.text):
        await message.answer("❌ Format noto‘g‘ri! Masalan: 15.05.1990")
        return
    try:
        day, month, year = map(int, message.text.replace("/", ".").split("."))
        datetime(year, month, day)  # faqat validatsiya
    except ValueError:
        await message.answer("❌ Sana noto‘g‘ri kiritildi!")
        return
    await state.update_data(date_of_birth=message.text)
    await message.answer("🏙️ Yashash shahringizni kiriting:")
    await state.set_state(HomeInsurance.city)

# Shahar
@router.message(HomeInsurance.city, F.text)
async def get_city(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 2:
        await message.answer("❌ Shahar nomi juda qisqa!")
        return
    await state.update_data(city=message.text.strip())
    await message.answer("📍 Manzilingizni kiriting (ko‘cha, uy raqami):")
    await state.set_state(HomeInsurance.address)

# Manzil
@router.message(HomeInsurance.address, F.text)
async def get_address(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 5:
        await message.answer("❌ Manzil juda qisqa!")
        return
    await state.update_data(address=message.text.strip())
    await message.answer("🏘️ Mol-mulk turini kiriting (Masalan: Kvartira, Hovli):")
    await state.set_state(HomeInsurance.property_type)

# Mulk turi + Tasdiq
@router.message(HomeInsurance.property_type, F.text)
async def get_property_type(message: types.Message, state: FSMContext):
    await state.update_data(property_type=message.text.strip())
    data = await state.get_data()

    await message.answer(
        f"📝 <b>Ma'lumotlaringizni tekshirib chiqing:</b>\n\n"
        f"👤 <b>F.I.O:</b> {data['full_name']}\n"
        f"📅 <b>Tug‘ilgan sana:</b> {data['date_of_birth']}\n"
        f"🏙️ <b>Shahar:</b> {data['city']}\n"
        f"📍 <b>Manzil:</b> {data['address']}\n"
        f"🏘️ <b>Mol-mulk turi:</b> {data['property_type']}\n\n"
        f"❓ Ushbu ma'lumotlarni tasdiqlaysizmi?",
        reply_markup=confirm_kb,
        parse_mode="HTML"
    )
    await state.set_state(HomeInsurance.confirm)

# Tasdiqlash
@router.message(HomeInsurance.confirm, F.text == "✅ Tasdiqlash")
async def confirm_home(message: types.Message, state: FSMContext):
    await message.answer("✅ Ma'lumotlar muvaffaqiyatli saqlandi! Mutaxassislar tez orada bog‘lanishadi.", reply_markup=main_menu_kb)
    await state.clear()

# Bekor qilish
@router.message(HomeInsurance.confirm, F.text == "❌ Bekor qilish")
async def cancel_home(message: types.Message, state: FSMContext):
    await message.answer("❌ Jarayon bekor qilindi.", reply_markup=main_menu_kb)
    await state.clear()

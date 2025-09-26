from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.auto import AutoInsurance
from keyboards.reply import main_menu_kb
import re
from datetime import datetime

router = Router()

# 🚗 Auto tugmasi bosilganda ishga tushadi
@router.message(F.text == "🚗 Auto")
async def auto_start(message: types.Message, state: FSMContext):
    # Avvalgi holatni tozalash
    await state.clear()
    
    await message.answer(
        "🚗 <b>Avtomobil sug'urtasi</b>\n\n"
        "Iltimos, ismingizni kiriting:",
        parse_mode='HTML'
    )
    await state.set_state(AutoInsurance.first_name)

# Ism qabul qilish
@router.message(AutoInsurance.first_name, F.text)
async def get_first_name(message: types.Message, state: FSMContext):
    if message.text == "🚗 Auto":
        return await auto_start(message, state)
    
    # Ismni tekshirish
    if len(message.text.strip()) < 2:
        await message.answer("❌ Ism kamida 2 ta harf bo'lishi kerak!")
        return
    
    await state.update_data(first_name=message.text.strip())
    await message.answer(
        "👤 Ism qabul qilindi ✅\n\n"
        "Familiyangizni kiriting:"
    )
    await state.set_state(AutoInsurance.last_name)

# Familiya qabul qilish
@router.message(AutoInsurance.last_name, F.text)
async def get_last_name(message: types.Message, state: FSMContext):
    if message.text == "🚗 Auto":
        return await auto_start(message, state)
    
    # Familiyani tekshirish
    if len(message.text.strip()) < 2:
        await message.answer("❌ Familiya kamida 2 ta harf bo'lishi kerak!")
        return
    
    await state.update_data(last_name=message.text.strip())
    await message.answer(
        "👤 Familiya qabul qilindi ✅\n\n"
        "Tug'ilgan sanangizni kiriting (format: DD.MM.YYYY yoki DD/MM/YYYY):\n"
        "Masalan: 15.05.1990 yoki 15/05/1990"
    )
    await state.set_state(AutoInsurance.date_of_birth)

# Tug'ilgan sana qabul qilish
@router.message(AutoInsurance.date_of_birth, F.text)
async def get_date_of_birth(message: types.Message, state: FSMContext):
    if message.text == "🚗 Auto":
        return await auto_start(message, state)
    
    # Sanani tekshirish
    date_pattern = r'^\d{1,2}[./]\d{1,2}[./]\d{4}$'
    if not re.match(date_pattern, message.text):
        await message.answer(
            "❌ Noto'g'ri format! \n\n"
            "To'g'ri format: DD.MM.YYYY yoki DD/MM/YYYY\n"
            "Masalan: 15.05.1990"
        )
        return
    
    # Sanani parse qilish
    try:
        date_str = message.text.replace('/', '.')
        day, month, year = map(int, date_str.split('.'))
        birth_date = datetime(year, month, day)
        
        # Yoshni tekshirish (16-100 yosh oralig'i)
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        if age < 16:
            await message.answer("❌ Yosh kamida 16 bo'lishi kerak!")
            return
        elif age > 100:
            await message.answer("❌ Noto'g'ri yil kiritilgan!")
            return
            
    except ValueError:
        await message.answer("❌ Noto'g'ri sana! Qaytadan kiriting:")
        return
    
    await state.update_data(date_of_birth=message.text)
    await message.answer(
        "📅 Tug'ilgan sana qabul qilindi ✅\n\n"
        "Yashayotgan shahringizni kiriting:"
    )
    await state.set_state(AutoInsurance.city)

# Shahar qabul qilish
@router.message(AutoInsurance.city, F.text)
async def get_city(message: types.Message, state: FSMContext):
    if message.text == "🚗 Auto":
        return await auto_start(message, state)
    
    if len(message.text.strip()) < 2:
        await message.answer("❌ Shahar nomi kamida 2 ta harf bo'lishi kerak!")
        return
    
    await state.update_data(city=message.text.strip())
    await message.answer(
        "🏙️ Shahar qabul qilindi ✅\n\n"
        "Ko'cha manzilini kiriting (raqam va ko'cha nomi):\n"
        "Masalan: 123 Main Street yoki Amir Temur ko'chasi 45-uy"
    )
    await state.set_state(AutoInsurance.street_address)

# Ko'cha manzili qabul qilish
@router.message(AutoInsurance.street_address, F.text)
async def get_street_address(message: types.Message, state: FSMContext):
    if message.text == "🚗 Auto":
        return await auto_start(message, state)
    
    if len(message.text.strip()) < 5:
        await message.answer("❌ Ko'cha manzili kamida 5 ta belgi bo'lishi kerak!")
        return
    
    await state.update_data(street_address=message.text.strip())
    await message.answer(
        "🏠 Ko'cha manzili qabul qilindi ✅\n\n"
        "Pochta indeksini (ZIP code) kiriting:\n"
        "Masalan: 100000 yoki 12345"
    )
    await state.set_state(AutoInsurance.zip_code)

# ZIP kod qabul qilish va yakuniy xabar
@router.message(AutoInsurance.zip_code, F.text)
async def get_zip_code(message: types.Message, state: FSMContext):
    if message.text == "🚗 Auto":
        return await auto_start(message, state)
    
    # ZIP kodni tekshirish
    if not message.text.strip().isdigit() or len(message.text.strip()) < 5:
        await message.answer("❌ ZIP kod kamida 5 ta raqam bo'lishi kerak!")
        return
    
    await state.update_data(zip_code=message.text.strip())
    
    # Barcha ma'lumotlarni olish
    data = await state.get_data()
    
    # Yakuniy xabar
    await message.answer(
        f"✅ <b>Barcha ma'lumotlar muvaffaqiyatli qabul qilindi!</b>\n\n"
        f"👤 <b>Ism:</b> {data['first_name']}\n"
        f"👤 <b>Familiya:</b> {data['last_name']}\n"
        f"📅 <b>Tug'ilgan sana:</b> {data['date_of_birth']}\n"
        f"🏙️ <b>Shahar:</b> {data['city']}\n"
        f"🏠 <b>Ko'cha manzili:</b> {data['street_address']}\n"
        f"📮 <b>ZIP kod:</b> {data['zip_code']}\n\n"
        f"📞 <b>Mutaxassislarimiz 24 soat ichida siz bilan bog'lanishadi!</b>\n\n"
        f"🔄 Boshqa xizmatlar uchun menyudan tanlang:",
        reply_markup=main_menu_kb,
        parse_mode='HTML'
    )
    await state.clear()

# Noto'g'ri formatdagi xabarlar uchun handler'lar
@router.message(AutoInsurance.first_name)
async def invalid_first_name(message: types.Message):
    await message.answer("❌ Iltimos, ismingizni faqat matn shaklida kiriting!")

@router.message(AutoInsurance.last_name)
async def invalid_last_name(message: types.Message):
    await message.answer("❌ Iltimos, familiyangizni faqat matn shaklida kiriting!")

@router.message(AutoInsurance.date_of_birth)
async def invalid_date_of_birth(message: types.Message):
    await message.answer("❌ Iltimos, tug'ilgan sanani to'g'ri formatda kiriting!")

@router.message(AutoInsurance.city)
async def invalid_city(message: types.Message):
    await message.answer("❌ Iltimos, shahar nomini matn shaklida kiriting!")

@router.message(AutoInsurance.street_address)
async def invalid_street_address(message: types.Message):
    await message.answer("❌ Iltimos, ko'cha manzilini matn shaklida kiriting!")

@router.message(AutoInsurance.zip_code)
async def invalid_zip_code(message: types.Message):
    await message.answer("❌ Iltimos, ZIP kodni raqam shaklida kiriting!")
import re
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from states.auto import AutoInsurance
from keyboards.reply import (
    gender_kb, marital_kb, education_kb,
    drivers_count_kb, cars_count_kb,
    ownership_kb, confirm_kb, phone_request_kb
)

router = Router()

# ----------------------- START -----------------------
# /auto komandasi yoki menyudagi "🚗 Auto" tugmasi bilan ishga tushadi
@router.message(Command("auto"))
@router.message(F.text == "🚗 Auto")
async def start_auto(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("👤 To‘liq ismingizni kiriting:")
    await state.set_state(AutoInsurance.full_name)


# ------------------- USER BASIC INFO -----------------
@router.message(AutoInsurance.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer("📅 Tug‘ilgan sana (MM/DD/YYYY):")
    await state.set_state(AutoInsurance.date_of_birth)


@router.message(AutoInsurance.date_of_birth)
async def get_dob(message: types.Message, state: FSMContext):
    await state.update_data(date_of_birth=message.text.strip())
    await message.answer("👤 Jinsingizni tanlang:", reply_markup=gender_kb)
    await state.set_state(AutoInsurance.gender)


@router.message(AutoInsurance.gender)
async def get_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text.strip())
    await message.answer("💍 Oilaviy ahvolingizni tanlang:", reply_markup=marital_kb)
    await state.set_state(AutoInsurance.marital_status)


@router.message(AutoInsurance.marital_status)
async def get_marital(message: types.Message, state: FSMContext):
    await state.update_data(marital_status=message.text.strip())
    await message.answer("🆔 SSN raqamingizni kiriting (9 ta raqam):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AutoInsurance.ssn)


@router.message(AutoInsurance.ssn)
async def get_ssn(message: types.Message, state: FSMContext):
    ssn = message.text.strip()
    if not ssn.isdigit() or len(ssn) != 9:
        await message.answer("❌ SSN 9 ta raqamdan iborat bo‘lishi kerak! Iltimos qayta kiriting.")
        return

    await state.update_data(ssn=ssn)
    await message.answer(
        "🏠 Manzilingizni kiriting\n\n"
        "📌 Example: <b>123 Wabash St, Pittsburgh, PA, 15205</b>",
        parse_mode="HTML"
    )
    await state.set_state(AutoInsurance.address)


@router.message(AutoInsurance.address)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await message.answer("📞 Telefon raqamingizni kiriting:", reply_markup=phone_request_kb)
    await state.set_state(AutoInsurance.phone)


@router.message(AutoInsurance.phone)
async def get_phone(message: types.Message, state: FSMContext):
    # Agar contact yuborilgan bo'lsa, contact dan olamiz
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text.strip()

    await state.update_data(phone=phone)
    await message.answer("📧 Emailingizni kiriting:")
    await state.set_state(AutoInsurance.email)


@router.message(AutoInsurance.email)
async def get_email(message: types.Message, state: FSMContext):
    email = message.text.strip()
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        await message.answer("❌ Email noto‘g‘ri formatda! Masalan: example@gmail.com")
        return

    await state.update_data(email=email)
    await message.answer("🎓 Ma’lumotingizni tanlang:", reply_markup=education_kb)
    await state.set_state(AutoInsurance.education)


@router.message(AutoInsurance.education)
async def get_education(message: types.Message, state: FSMContext):
    await state.update_data(education=message.text.strip())
    await message.answer("🚘 Haydovchilik guvohnomasi raqamini kiriting:")
    await state.set_state(AutoInsurance.license_number)


# 2️⃣ Driver Info (asosiy haydovchi)
@router.message(AutoInsurance.license_number)
async def get_license_number(message: types.Message, state: FSMContext):
    await state.update_data(license_number=message.text.strip())
    await message.answer("📅 Guvohnoma amal qilish muddati (MM/DD/YYYY):")
    await state.set_state(AutoInsurance.license_expiration)


@router.message(AutoInsurance.license_expiration)
async def get_license_exp(message: types.Message, state: FSMContext):
    date = message.text.strip()
    pattern = r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/[0-9]{4}$"
    if not re.match(pattern, date):
        await message.answer("❌ Format noto‘g‘ri!\n📌 To‘g‘ri misol: <b>08/25/2027</b>", parse_mode="HTML")
        return

    await state.update_data(license_expiration=date)
    await message.answer("🎂 Birinchi guvohnoma olgan yosh:")
    await state.set_state(AutoInsurance.first_license_age)


@router.message(AutoInsurance.first_license_age)
async def get_first_license_age(message: types.Message, state: FSMContext):
    age_text = message.text.strip()
    if not age_text.isdigit() or int(age_text) < 14 or int(age_text) > 100:
        await message.answer("❌ Yosh noto‘g‘ri! (14–100 oralig‘ida bo‘lishi kerak)")
        return

    await state.update_data(first_license_age=age_text)
    await message.answer("🏛 Qaysi shtatda guvohnoma olingan?")
    await state.set_state(AutoInsurance.first_license_state)


@router.message(AutoInsurance.first_license_state)
async def get_first_license_state(message: types.Message, state: FSMContext):
    await state.update_data(first_license_state=message.text.strip())
    await message.answer("👥 Uyda nechta haydovchi bor?", reply_markup=drivers_count_kb)
    await state.set_state(AutoInsurance.drivers_count)


# ------------------- DRIVERS INFO (Qo'shimcha haydovchilar) --------------------
@router.message(AutoInsurance.drivers_count)
async def get_drivers_count(message: types.Message, state: FSMContext):
    text = message.text.replace("👥", "").replace("🚫", "").strip()
    if text.isdigit():
        count = int(text)
    elif "yo‘q" in text.lower() or "yoq" in text.lower():
        count = 0
    else:
        await message.answer("❌ Iltimos, son kiriting yoki 🚫 Yo‘q tugmasini bosing.")
        return

    await state.update_data(drivers_count=count, current_driver=1, drivers=[])
    if count > 0:
        await message.answer("👤 1-haydovchining to‘liq ismini kiriting:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AutoInsurance.driver_fullname)
    else:
        await message.answer("🚗 Uyda nechta mashina bor?", reply_markup=cars_count_kb)
        await state.set_state(AutoInsurance.cars_count)


@router.message(AutoInsurance.driver_fullname)
async def get_driver_fullname(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_driver = data.get("current_driver", 1)
    driver_info = {"fullname": message.text.strip()}
    drivers = data.get("drivers", [])
    drivers.append(driver_info)
    await state.update_data(drivers=drivers)
    await message.answer(f"📅 {current_driver}-haydovchining tug‘ilgan sanasini kiriting (MM/DD/YYYY):")
    await state.set_state(AutoInsurance.driver_dob)


@router.message(AutoInsurance.driver_dob)
async def get_driver_dob(message: types.Message, state: FSMContext):
    data = await state.get_data()
    drivers = data.get("drivers", [])
    drivers[-1]["dob"] = message.text.strip()
    await state.update_data(drivers=drivers)
    current_driver = data.get("current_driver", 1)
    await message.answer(f"📅 {current_driver}-haydovchining guvohnoma amal qilish muddati (MM/DD/YYYY):")
    await state.set_state(AutoInsurance.driver_license_exp)


@router.message(AutoInsurance.driver_license_exp)
async def get_driver_license_exp(message: types.Message, state: FSMContext):
    data = await state.get_data()
    drivers = data.get("drivers", [])
    drivers[-1]["license_exp"] = message.text.strip()
    await state.update_data(drivers=drivers)
    current_driver = data.get("current_driver", 1)
    await message.answer(f"🎂 {current_driver}-haydovchi birinchi guvohnoma olgan yosh:")
    await state.set_state(AutoInsurance.driver_first_age)


@router.message(AutoInsurance.driver_first_age)
async def get_driver_first_age(message: types.Message, state: FSMContext):
    data = await state.get_data()
    drivers = data.get("drivers", [])
    drivers[-1]["first_age"] = message.text.strip()
    await state.update_data(drivers=drivers)
    current_driver = data.get("current_driver", 1)
    await message.answer(f"🏛 {current_driver}-haydovchi qaysi shtatda guvohnoma olgan?")
    await state.set_state(AutoInsurance.driver_first_state)


@router.message(AutoInsurance.driver_first_state)
async def get_driver_first_state(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_driver = data.get("current_driver", 1)
    drivers = data.get("drivers", [])
    drivers[-1]["first_state"] = message.text.strip()
    await state.update_data(drivers=drivers)

    if current_driver < data.get("drivers_count", 0):
        next_driver = current_driver + 1
        await state.update_data(current_driver=next_driver)
        await message.answer(f"👤 {next_driver}-haydovchining to‘liq ismini kiriting:")
        await state.set_state(AutoInsurance.driver_fullname)
    else:
        await message.answer("🚗 Uyda nechta mashina bor?", reply_markup=cars_count_kb)
        await state.set_state(AutoInsurance.cars_count)


# ------------------- CARS INFO -----------------------
@router.message(AutoInsurance.cars_count)
async def get_cars_count(message: types.Message, state: FSMContext):
    text = message.text.strip()

    # ➕ Boshqa son tugmasi bosilganda — foydalanuvchidan raqam kiritishni so'raymiz
    if text == "➕ Boshqa son":
        await message.answer("✍️ Mashinalar sonini yozib yuboring (raqam bilan, kamida 1):", reply_markup=types.ReplyKeyboardRemove())
        return  # keyingi xabarida foydalanuvchi son yuboradi

    # Agar tugma orqali 1-5 raqamlardan biri bosilgan bo'lsa
    if text.isdigit():
        count = int(text)
    else:
        await message.answer("❌ Iltimos, 1 dan boshlab haqiqiy son kiriting yoki ➕ Boshqa son tugmasini bosing.")
        return

    # Endi 0 yoki manfiyni qabul qilmaymiz — kamida 1 bo'lishi shart
    if count < 1:
        await message.answer("❌ Sug'urta uchun kamida 1 ta mashina kerak. Iltimos, kamida 1 ni tanlang yoki yozib yuboring.")
        return

    # State ga saqlash va jarayonni boshlash
    await state.update_data(cars_count=count, current_car=1, cars=[])

    await message.answer("🚗 1-mashinaning markasini kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AutoInsurance.car_make)



@router.message(AutoInsurance.car_make)
async def get_car_make(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_car = data.get("current_car", 1)
    car_info = {"make": message.text.strip()}
    cars = data.get("cars", [])
    cars.append(car_info)
    await state.update_data(cars=cars)
    await message.answer(f"📅 {current_car}-mashinaning yilini kiriting:")
    await state.set_state(AutoInsurance.car_year)


@router.message(AutoInsurance.car_year)
async def get_car_year(message: types.Message, state: FSMContext):
    year = message.text.strip()
    if not year.isdigit() or not (1900 <= int(year) <= 2100):
        await message.answer("❌ Yil noto‘g‘ri! Masalan: 2015")
        return

    data = await state.get_data()
    cars = data.get("cars", [])
    cars[-1]["year"] = year
    await state.update_data(cars=cars)
    current_car = data.get("current_car", 1)
    await message.answer(f"🔢 {current_car}-mashinaning davlat raqamini kiriting:")
    await state.set_state(AutoInsurance.car_number)


@router.message(AutoInsurance.cars_count, F.text.regexp(r"^\d+$"))
async def get_cars_count_custom(message: types.Message, state: FSMContext):
    count = int(message.text.strip())
    if count < 1:
        await message.answer("❌ Sug'urta uchun kamida 1 ta mashina kerak. Iltimos, yana kiriting (kamida 1).")
        return

    await state.update_data(cars_count=count, current_car=1, cars=[])
    await message.answer("🚗 1-mashinaning markasini kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AutoInsurance.car_make)



@router.message(AutoInsurance.car_number)
async def get_car_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cars = data.get("cars", [])
    cars[-1]["number"] = message.text.strip()
    await state.update_data(cars=cars)
    current_car = data.get("current_car", 1)
    await message.answer(f"⚖️ {current_car}-mashinaning egalik turini tanlang:", reply_markup=ownership_kb)
    await state.set_state(AutoInsurance.car_ownership)


@router.message(AutoInsurance.car_ownership)
async def get_car_ownership(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cars = data.get("cars", [])
    cars[-1]["ownership"] = message.text.strip()
    await state.update_data(cars=cars)

    if data.get("current_car", 1) < data.get("cars_count", 0):
        next_car = data["current_car"] + 1
        await state.update_data(current_car=next_car)
        await message.answer(f"🚗 {next_car}-mashinaning markasini kiriting:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AutoInsurance.car_make)
    else:
        await show_summary(message, await state.get_data(), state)


# ------------------- SUMMARY -------------------------
async def show_summary(message: types.Message, data: dict, state: FSMContext):
    summary = (
        "📑 <b>Auto Insurance Ma’lumotlaringiz</b>\n\n"
        f"👤 Ism: <b>{data.get('full_name')}</b>\n"
        f"📅 Tug‘ilgan sana: <b>{data.get('date_of_birth')}</b>\n"
        f"👤 Jinsi: <b>{data.get('gender')}</b>\n"
        f"💍 Oilaviy ahvol: <b>{data.get('marital_status')}</b>\n"
        f"🆔 SSN: <b>{data.get('ssn')}</b>\n"
        f"🏠 Manzil: <b>{data.get('address')}</b>\n"
        f"📞 Telefon: <b>{data.get('phone')}</b>\n"
        f"📧 Email: <b>{data.get('email')}</b>\n"
        f"🎓 Ma’lumoti: <b>{data.get('education')}</b>\n"
        f"🚘 Prava raqami: <b>{data.get('license_number')}</b>\n"
        f"📅 Amal qilish muddati: <b>{data.get('license_expiration')}</b>\n"
        f"🎂 Birinchi prava olgan yosh: <b>{data.get('first_license_age')}</b>\n"
        f"🏛 Qaysi shtatda olingan: <b>{data.get('first_license_state')}</b>\n\n"
    )

    drivers = data.get("drivers", [])
    if drivers:
        summary += "👥 <b>Qo‘shimcha haydovchilar:</b>\n"
        for idx, d in enumerate(drivers, 1):
            summary += (
                f"   {idx}. {d.get('fullname','-')} ({d.get('dob','-')})\n"
                f"      📅 Guvohnoma muddati: {d.get('license_exp','-')}\n"
                f"      🎂 Birinchi yosh: {d.get('first_age','-')}\n"
                f"      🏛 Shtat: {d.get('first_state','-')}\n"
            )
        summary += "\n"

    cars = data.get("cars", [])
    if cars:
        summary += "🚗 <b>Mashinalar:</b>\n"
        for idx, c in enumerate(cars, 1):
            summary += (
                f"   {idx}. {c.get('make','-')} ({c.get('year','-')})\n"
                f"      🔢 Raqami: {c.get('number','-')}\n"
                f"      ⚖️ Egalik: {c.get('ownership','-')}\n"
            )
        summary += "\n"

    summary += "✅ Ma’lumotlarni tasdiqlaysizmi?"

    await message.answer(summary, parse_mode="HTML", reply_markup=confirm_kb)
    await state.set_state(AutoInsurance.confirm)


# ✅ Tasdiqlash yoki ❌ Bekor qilish
@router.message(AutoInsurance.confirm, F.text == "✅ Tasdiqlash")
async def confirm_data(message: types.Message, state: FSMContext):
    await message.answer("✅ Ma’lumotlaringiz saqlandi!", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


@router.message(AutoInsurance.confirm, F.text == "❌ Bekor qilish")
async def cancel_data(message: types.Message, state: FSMContext):
    await message.answer("❌ Jarayon bekor qilindi!", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

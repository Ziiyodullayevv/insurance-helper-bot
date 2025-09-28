from aiogram.fsm.state import StatesGroup, State

class AutoInsurance(StatesGroup):
    # 1️⃣ Asosiy haydovchi ma'lumotlari
    full_name = State()
    date_of_birth = State()
    gender = State()
    marital_status = State()
    ssn = State()
    address = State()
    phone = State()
    email = State()
    education = State()

    # 🚘 Driver info
    license_number = State()
    license_expiration = State()
    first_license_age = State()
    first_license_state = State()

    # 👥 Uy haydovchilari
    drivers_count = State()
    driver_fullname = State()
    driver_dob = State()
    driver_license_exp = State()
    driver_first_age = State()
    driver_first_state = State()

    # 🚗 Car info
    cars_count = State()
    car_make = State()       # mashina markasi (Toyota, Honda, Ford…)
    car_year = State()       # mashina yili
    car_number = State()     # mashina davlat raqami
    car_ownership = State()  # egalik turi (sotib olingan, kredit, ijaraga)

    # ✅ Yakuniy tasdiqlash
    confirm = State()

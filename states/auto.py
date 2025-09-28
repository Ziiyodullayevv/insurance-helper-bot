from aiogram.fsm.state import StatesGroup, State

class AutoInsurance(StatesGroup):
    first_name = State()        # Ism
    last_name = State()         # Familiya
    date_of_birth = State()     # Tug'ilgan sana
    city = State()              # Shahar
    street_address = State()    # Ko'cha raqami va nomi
    zip_code = State()          # Pochta indeksi
    confirm = State()  
from aiogram.fsm.state import StatesGroup, State

class LifeInsurance(StatesGroup):
  full_name = State()
  date_of_birth = State()
  phone_number = State()
  city = State()
  confirm = State()

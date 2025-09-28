from aiogram.fsm.state import StatesGroup, State

class HomeInsurance(StatesGroup):
  full_name = State()
  date_of_birth = State()
  city = State()
  address = State()
  property_type = State()
  confirm = State()



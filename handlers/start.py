from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards.reply import main_menu_kb

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    # Foydalanuvchi ismini xavfsiz olish
    name = message.from_user.first_name or "Foydalanuvchi"
    
    await message.answer(
        f"👋 Salom, {name}!\n\n"
        f"🛡️ InsuranceHelper Botga xush kelibsiz!\n\n"
        f"📋 Men sizga quyidagilar bilan yordam bera olaman:\n\n"
        f"• 🚗 Avtomobil sug'urtasi bo'yicha maslahat\n"
        f"• 🏠 Uy-joy sug'urtasi to'g'risida\n"
        f"• 💼 Hayot sug'urtasi maslahatlari\n"
        f"• 📞 Sug'urta kompaniyalari bilan bog'lanish\n"
        f"• 💡 Sug'urta masalalari bo'yicha konsultatsiya\n\n"
        f"🔽 Kerakli bo'limni tanlang:",
        reply_markup=main_menu_kb
    )
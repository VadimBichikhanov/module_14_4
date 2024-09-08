from sre_parse import State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import Form
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
class CalorieCalculator(Form):
    def __init__(self, state: FSMContext):
        super().__init__()
        self.state = state

    async def set_gender(self, message: Message):
        inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Женщина", callback_data="female")],
                [InlineKeyboardButton(text="Мужчина", callback_data="male")]
            ]
        )
        await message.answer("Выберите ваш пол:", reply_markup=inline_keyboard)

    async def set_age(self, call: CallbackQuery):
        await self.state.update_data(gender=call.data)
        await call.message.answer("Пожалуйста, введите ваш возраст:")
        await self.state.set_state(Form.age)
        await call.answer()

    async def process_numeric_input(self, message: Message, key: str, prompt: str, next_state: State, callback=None):
        try:
            value = int(message.text)
            await self.state.update_data(**{key: value})
            if callback:
                await callback(message)
            else:
                await message.reply(prompt)
                await self.state.set_state(next_state)
        except ValueError:
            await message.reply('Пожалуйста, введите корректное число.')
            await self.state.set_state(next_state)  # Сброс состояния в случае ошибки

    async def calculate_calories(self, message: Message):
        data = await self.state.get_data()
        if 'gender' not in data or 'age' not in data or 'growth' not in data or 'weight' not in data:
            await message.reply("Недостаточно данных для расчета калорий.")
            return
        age = data['age']
        growth = data['growth']
        weight = data['weight']
        gender = data['gender']

        if gender == "female":
            # Формула Миффлина - Сан Жеора для женщин
            calories = 10 * weight + 6.25 * growth - 5 * age - 161
        elif gender == "male":
            # Формула Миффлина - Сан Жеора для мужчин
            calories = 10 * weight + 6.25 * growth - 5 * age + 5
        else:
            await message.reply("Неизвестный пол.")
            return

        # Расчет БЖУ
        proteins = weight * 2  # Примерно 2 грамма белка на килограмм веса
        fats = weight * 1  # Примерно 1 грамм жира на килограмм веса
        carbs = (calories - (proteins * 4 + fats * 9)) / 4  # Углеводы рассчитываются по остатку калорий

        await message.reply(f'Ваша норма калорий: {calories:.2f} ккал в день.\n'
                            f'Белки: {proteins:.2f} г\n'
                            f'Жиры: {fats:.2f} г\n'
                            f'Углеводы: {carbs:.2f} г')
        await self.state.clear()
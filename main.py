import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import CurrencyState
from exchange import get_currency
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("rates"))
async def cmd_rates(message: types.Message, state: FSMContext):
    await message.answer("Напишите 3-хзначный код вашей желаемой валюты:")
    await state.set_state(CurrencyState.waiting_for_code)


@dp.message(CurrencyState.waiting_for_code)
async def process_currency_code(message: types.Message, state: FSMContext):
    code = message.text.upper()

    data = await get_currency()

    if data is None:
        await message.answer("Не удалось получить данные. Попробуйте позже.")
        await state.clear()
        return

    valute = data["Valute"]

    if code not in valute:
        await message.answer("Валюта не найдена.")
        return  # состояние НЕ сбрасываем — пользователь может ввести код ещё раз

    currency = valute[code]
    name = currency["Name"]
    value = currency["Value"]
    previous = currency["Previous"]

    answer_text = (
        f"Валюта: {name} ({code})\n"
        f"Текущий курс: {value:.2f} руб.\n"
        f"Предыдущий курс: {previous:.2f} руб."
    )

    await message.answer(answer_text)
    await state.clear()

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
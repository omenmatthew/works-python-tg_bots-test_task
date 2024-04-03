from aiogram import types, Bot, Dispatcher, filters, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
import asyncio
import re

logging.basicConfig(level=logging.INFO)
TOKEN = "7103361320:AAH0WNtgimKx7w_qAsAdnbmRQD67iASznzU"
dp = Dispatcher()
bot = Bot(token=TOKEN)

class StatesClass(StatesGroup):
    name_state = State()
    number_state = State()
    comment_state = State()
    agreement_state = State()


@dp.message(filters.CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    await message.answer(f"{message.from_user.full_name}, Добро пожаловать в компанию DamnIT!")
    await message.answer("Напишите свое ФИО")
    await state.clear()
    await state.set_state(StatesClass.name_state)

@dp.message(StatesClass.name_state)
async def name_message_handler(message: types.Message, state: FSMContext):
    if any(ch.isdigit() for ch in message.text):
        await message.reply("В имени должны отсутствовать цифры")
        # await state.set_state(StatesClass.name_state)
    else:
        await state.update_data(name_state=message.text)
        await message.answer("Укажите Ваш номер телефона в формате 7 XXX XXX XX XX")
        await state.set_state(StatesClass.number_state)

@dp.message(StatesClass.number_state)
async def name_message_handler(message: types.Message, state: FSMContext):
    is_valid_phone_number = lambda num: bool(re.match(r'^7 \d{3} \d{3} \d{2} \d{2}$', num))
    if not is_valid_phone_number(message.text):
        await message.reply("Неверный формат ввода")
        # await state.set_state(StatesClass.number_state_state)
    else:
        await state.update_data(number_state=message.text)
        await message.answer("Напишите любой комментарий")
        await state.set_state(StatesClass.comment_state)

@dp.message(StatesClass.comment_state)
async def name_message_handler(message: types.Message, state: FSMContext):
    await state.update_data(comment_state=message.text)
    comment_file = FSInputFile("test.pdf")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Далее", callback_data="next_button"))
    await message.answer("Последний шаг! Ознакомься с вводными положениями")
    await message.answer_document(comment_file, reply_markup=builder.as_markup())
    await state.set_state(StatesClass.agreement_state)

@dp.callback_query(F.data == "next_button")
async def next_step_agreement(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="ДА!", callback_data="yes_button"))
    await callback.message.answer("Ознакомился", reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data == "yes_button")
async def next_step_agreement(callback: types.CallbackQuery, state: FSMContext):
    img = FSInputFile("photo_2024-04-01_21-16-30.jpg")
    data = await state.get_data()
    name = data.get('name_state', '')
    phone = data.get('number_state', '')
    comment = data.get('comment_state', '')
    await callback.message.answer_photo(img, caption="Спасибо за успешную регистрацию")
    await callback.answer()
    my_id = '1652139347'
    await bot.send_message(my_id, f"Новая заявка: {name}, {phone}, {comment}")
    state.clear()



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

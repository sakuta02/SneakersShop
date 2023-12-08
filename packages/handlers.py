from aiogram import Router
from packages.filters_states import Brand, Boot, Buy, add_to_packet, get_from_basket, delete_from_basket
from packages.localization import phrases
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from packages.keyboards import keyboard_start, button_size, keyboard_sizes, keyboard_menu

rt = Router()
users_data = {}


@rt.message(Command(commands=['start']), StateFilter(default_state))
async def greetings(message: Message):
    await message.answer(text=phrases["start"], reply_markup=keyboard_start)


@rt.callback_query(Brand(), StateFilter(default_state))
async def send_brand(callback: CallbackQuery, key):
    await callback.message.edit_text(text=phrases["model"], reply_markup=key)


@rt.callback_query(Boot(), StateFilter(default_state))
async def send_photo(callback: CallbackQuery, path, name, id_b, state: FSMContext):
    await callback.message.answer_photo(photo=path, caption=(f"<b>{name}</b>" + f"\nЦена: {(len(name) * 200) % 15000}р.\n" + phrases["parcel"]),
                                        reply_markup=button_size)
    await callback.message.delete()
    await state.set_state(Buy.choose_size)
    users_data[callback.from_user.id] = {"id_b": id_b, "name": name}


@rt.callback_query(StateFilter(Buy.choose_size), lambda x: x.data != "MENU")
async def send_sizes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(caption=phrases["size"], reply_markup=keyboard_sizes)
    await state.set_state(default_state)


@rt.callback_query(StateFilter(default_state), lambda x: int(x.data[:2]) in range(40, 50) if x.data[:2].isdigit()
        else False)
async def get_size(callback: CallbackQuery):
    temp_dict, size = users_data[callback.from_user.id], int(callback.data[:2])
    add_to_packet(size, temp_dict["name"], callback.from_user.id, int(temp_dict["id_b"]))
    await callback.message.delete()
    await callback.message.answer(phrases["basket"], reply_markup=keyboard_menu)


@rt.message(Command(commands=['basket']))
async def show_basket(message: Message):
    value = get_from_basket(int(message.from_user.id))
    total_string = []
    total_price = 0
    for i in range(len(value)):
        boots = value[i]
        total_price += boots[-2]
        total_string.append(f"Номер в корзине: {boots[-1]}\nРазмер: {boots[0]}\nНазвание: {boots[1]}\nЦена: {boots[-2]}р")
    await message.answer(text=('\n\n'.join(total_string) + f'\n\nИтого: {total_price}р'
                               '\n\n\nЧтобы удалить товр из корзины введите \n"/del (номер товара в корзине)"'))


@rt.message(Command(commands=["del"]))
async def delete_from_basket_func(message: Message):
    id_user = int(message.from_user.id)
    delete_from_basket(int(message.text[4:]), id_user)


@rt.callback_query(lambda x: x.data == "MENU")
async def send_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    if callback.from_user.id in users_data:
        del users_data[callback.from_user.id]
    try:
        await callback.message.edit_text(text=phrases["menu"], reply_markup=keyboard_start)
    except:
        await callback.message.delete()
        await callback.message.answer(text=phrases["menu"], reply_markup=keyboard_start)

from packages.localization import buttons
import sqlite3 as sql
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


'''start'''
start = []
for text, data in buttons["start"]:
    start.append([InlineKeyboardButton(text=text, callback_data=data)])
keyboard_start = InlineKeyboardMarkup(inline_keyboard=start)

'''Menu'''
button_menu = [InlineKeyboardButton(text="Меню📃", callback_data="MENU")]
keyboard_menu = InlineKeyboardMarkup(inline_keyboard=[button_menu])

'''adidas'''
obj = [list(map(lambda x: InlineKeyboardButton(text=x[0], callback_data=x[1]), buttons["move_a"]))]
with sql.connect(r'./purchases.db') as db:
    cur = db.cursor()
    cur.execute("SELECT name, id FROM shoes WHERE brand like 'Adidas'")
    temp = cur.fetchall()
    a_buttons_first = temp
a_buttons_first = (list(map(lambda x: [InlineKeyboardButton(text=x[0], callback_data=str(x[1]))],
                            a_buttons_first)) + obj + [button_menu])
keyboard_adidas_1 = InlineKeyboardMarkup(inline_keyboard=a_buttons_first + [])


'''NIKE'''
obj = [list(map(lambda x: InlineKeyboardButton(text=x[0], callback_data=x[1]), buttons["move_n"]))]
with sql.connect(r'./purchases.db') as db:
    cur = db.cursor()
    cur.execute("SELECT name, id FROM shoes WHERE brand like 'NIKE'")
    temp = cur.fetchall()
    n_buttons_first = temp
n_buttons_first = (list(map(lambda x: [InlineKeyboardButton(text=x[0], callback_data=str(x[1]))],
                            n_buttons_first)) + obj + [button_menu])
keyboard_nike_1 = InlineKeyboardMarkup(inline_keyboard=n_buttons_first)


'''BALANCE'''
obj = [list(map(lambda x: InlineKeyboardButton(text=x[0], callback_data=x[1]), buttons["move_new"]))]
with sql.connect(r'./purchases.db') as db:
    cur = db.cursor()
    cur.execute("SELECT name, id FROM shoes WHERE brand like 'BALANCE'")
    temp = cur.fetchall()
    new_buttons_first = temp
new_buttons_first = (list(map(lambda x: [InlineKeyboardButton(text=x[0], callback_data=str(x[1]))],
                              new_buttons_first)) + obj + [button_menu])
keyboard_new_1 = InlineKeyboardMarkup(inline_keyboard=new_buttons_first)


"""BUY THAT ONE"""
button_size = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=buttons["size"][0],
                                                                          callback_data=buttons["size"][1])],
                                                    button_menu])

'''size'''
temp = list(map(lambda x: InlineKeyboardButton(text=str(x[0]), callback_data=x[1]), buttons["sizes"]))
keyboard_sizes = InlineKeyboardMarkup(inline_keyboard=[temp[:3], temp[3:], button_menu])


'''cities'''
temp = list(map(lambda x: InlineKeyboardButton(text=x[0], callback_data=x[1]), buttons["cities"]))
keyboard_cities = InlineKeyboardMarkup(inline_keyboard=[temp[:2], temp[2:], button_menu])

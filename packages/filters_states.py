from aiogram.filters import BaseFilter
from packages.keyboards import keyboard_adidas_1, keyboard_nike_1, keyboard_new_1
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
import sqlite3 as sql


class Buy(StatesGroup):
    choose_size = State()


class Brand(BaseFilter):
    data = {"ADIDAS": keyboard_adidas_1,
            "BackAd": keyboard_new_1,
            "NextAd": keyboard_nike_1,
            "NIKE": keyboard_nike_1,
            "BackNike": keyboard_adidas_1,
            "NextNike": keyboard_new_1,
            "NextNew": keyboard_adidas_1,
            "BackNew": keyboard_nike_1,
            "BALANCE": keyboard_new_1
            }

    async def __call__(self, callback: CallbackQuery):
        if callback.data in self.data:
            return {"key": self.data[callback.data]}
        return False


class Boot(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        try:
            id_b = int(callback.data)
            with sql.connect(r'./purchases.db') as db:
                cur = db.cursor()
                cur.execute(f'SELECT path, name FROM shoes WHERE id like {id_b}')
                values = cur.fetchall()
                return {'path': values[0][0], 'name': values[0][1], 'id_b': id_b}
        except ValueError:
            return False


def add_to_packet(size: int, model: str, id_user: int, id_boots: int):
    with sql.connect(r'./purchases.db') as db:
        cur = db.cursor()
        cur.execute(f"SELECT name FROM shoes WHERE id={id_boots}")
        v = cur.fetchall()
        price = (len(v[0][0]) * 200)
        cur.execute(f"INSERT INTO basket VALUES({size}, '{model}', {id_user}, {id_boots}, {price})")


def get_from_basket(id_user: int):
    with sql.connect(r'./purchases.db') as db:
        cur = db.cursor()
        cur.execute(f"SELECT size, model, id_user, id_boots, price, rowid FROM basket WHERE id_user like {id_user}")
        value = cur.fetchall()
        return value


def delete_from_basket(rowid, id_user):
    with sql.connect(r'./purchases.db') as db:
        cur = db.cursor()
        cur.execute(f"DELETE FROM basket WHERE rowid={rowid} AND id_user={id_user}")

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bd import db_participant
from bd.db_participant import Database_participant
from config import *
from bd.db_raffle import Database_raffle
from profile import Raffle, Raffle_Edit, Raffle_Choose, Raffle_Stop, Raffle_Rerol

db_raffle = Database_raffle()
db_par = Database_participant()

def add_user(user_id, msg_id):
    # if db_raffle.get_user_id(user_id, msg_id):
    #     return False

    # else:
        if db_par.get_max_id1() == None:
            conf_inline1 = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Принять участие (0)",
                        callback_data=Raffle(msg_id=msg_id, status=0).pack()
                    )
                ]
            ])
            return conf_inline1

        else:
            conf_inline1 = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Принять участие ({db_par.get_count_users(msg_id)})",
                        callback_data=Raffle(msg_id=msg_id, status=0).pack())
                ]
            ])
            return conf_inline1

#
# conf_inline2 = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(
#             text=f"Принять участие {db_raffle.get_max_id()}",
#             callback_data="raffle_close")
#     ]
# ])

prise = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=f"ЛК",
            callback_data="prise_lc"),
        InlineKeyboardButton(
            text=f"Ник",
            callback_data="prise_server")
    ]
])

conf_inline3 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=f"Перекрутить",
            callback_data="raffle_rerol"),
        InlineKeyboardButton(
            text=f"Сообщить",
            callback_data="raffle_noti")
    ]
])


# conk = InlineKeyboardMarkup(row_width=1)
# join = InlineKeyboardButton(text="Принять участие (0)", callback_data="raffle_join")
# conk.add(join)


sure = InlineKeyboardBuilder()
sure.button(text="Подтвердить", callback_data="raffle_sure"),
sure.button(text="Отменить", callback_data="raffle_cancel")
sure.adjust(1)
sure = sure.as_markup()

def raffle(count):
    raffle = InlineKeyboardBuilder()
    if count == None:
        count = 1
    for i in range(1, count+1):
        # try:
        name = db_raffle.get_name(id=i)
        raffle.button(text=f"{name}", callback_data=Raffle_Edit(msg_id=db_raffle.get_msg_id(name), id=i, status=1))
        # except:
        #     pass
    raffle.adjust(1)
    raffle = raffle.as_markup()
    return raffle

def random_win(msg_id, id, raffle_id):
    random_win = InlineKeyboardBuilder()
    random_win.button(text="Выбрать победителей", callback_data=Raffle_Choose(msg_id=msg_id, status=2, id=id, command="choose", raffle_id=raffle_id))
    random_win.button(text="Удалить всех участников", callback_data=Raffle_Choose(msg_id=msg_id, status=2, id=id, command="del", raffle_id=raffle_id))
    random_win.button(text="Назад", callback_data=Raffle_Choose(msg_id=msg_id, status=2, id=id, command="back", raffle_id=raffle_id))
    random_win.adjust(1)
    random_win = random_win.as_markup()
    return random_win

def confirm_buttons(msg_id, id, raffle_id):
    rerol = InlineKeyboardBuilder()
    rerol.button(text="Рерол", callback_data=Raffle_Rerol(msg_id=msg_id, status=4, id=id, action="rerol", raffle_id=raffle_id))
    rerol.button(text="Подтвердить", callback_data=Raffle_Rerol(msg_id=msg_id, status=4, id=id, action="post", raffle_id=raffle_id))
    rerol.adjust(1)
    rerol = rerol.as_markup()
    return rerol

def select(msg_id):
    select = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить", callback_data=Raffle_Stop(status=3, msg_id=msg_id).pack())
        ]
    ])
    return select

def stop_raffle(msg_id):
    conf_inline1 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"Принять участие ({db_raffle.get_count_users(msg_id)})", callback_data="stop"
            )
        ]
    ])
    return conf_inline1

chanel_link = InlineKeyboardBuilder()
chanel_link.button(text="Перейти на наш канал", url=f"https://t.me/{chanel_username}")
chanel_link.button(text="Проверить снова", url=f"https://t.me/{bot_username}?start=start")
chanel_link.adjust(1)
chanel_link = chanel_link.as_markup()


confirm = InlineKeyboardBuilder()
confirm.button(text="Подтвердить", callback_data="confirm_confirm")
confirm.button(text="Изменить", callback_data="confirm_edit")
confirm.adjust(1)
confirm = confirm.as_markup()


get_prise_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Забрать приз", url=f"https://t.me/{bot_username}?start=start")
    ]
])
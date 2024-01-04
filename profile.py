from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State

from config import admins


def check_sub_channel(chat_member, user_id):
    if chat_member.status != "left":#and db_language.get_ban_id(user_id) != "ban":
        # print(chat_member.status)
        return True
    else:
        return False

# db_raffle.drop_table()
# db_raffle.create_table()
# db_raffle.add_user(1)
# if db_raffle.get_user_id(1):
#     print(1)
# else:
#     print(2)

class FSMAdmin_raffle(StatesGroup):
    name = State()
    type = State()
    prise = State()
    prise_id = State()
    prise_loser = State()
    prise_loser_id = State()
    raffle = State()
    sure = State()

class Set_Nick(StatesGroup):
    name = State()
    confirm = State()

class Set_Email(StatesGroup):
    email = State()
    confirm = State()
class Raffle(CallbackData, prefix=""):
    status: int
    msg_id: int

class Raffle_Edit(CallbackData, prefix=""):
    status: int
    msg_id: int
    id: int

class Raffle_Choose(CallbackData, prefix=""):
    status: int
    msg_id: int
    id: int
    command: str
    raffle_id: int


class Raffle_Stop(CallbackData, prefix=""):
    status: int
    msg_id: int

class Raffle_Rerol(CallbackData, prefix=""):
    status: int
    msg_id: int
    id: int
    action: str
    raffle_id: int



def check_admin(user_id):
    if user_id in admins:
        return True


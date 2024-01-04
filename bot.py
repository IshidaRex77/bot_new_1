import asyncio
import io
import os
import random

import requests
from PIL import Image
from aiogram import *
from aiogram.enums import ParseMode
from aiogram import F
from aiogram.types import *
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from bd.db_participant import Database_participant
from bd.db_server import Database_server
from bd.db_winner import Database_winner
from bd.db_winner_arhive import Database_winner_archive
from config import *
from bd.db_raffle import Database_raffle
from keyboards import sure, add_user, raffle, random_win, select, stop_raffle, prise, confirm_buttons, chanel_link, \
    confirm, get_prise_button
from profile import FSMAdmin_raffle, check_sub_channel, Raffle, Raffle_Edit, Raffle_Choose, Raffle_Stop, Raffle_Rerol, \
    Set_Nick, Set_Email

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
form_router = Router()
state = State
db_raffle = Database_raffle()
db_par = Database_participant()
db_winner = Database_winner()
db_winner_archive = Database_winner_archive()
db_server = Database_server()


# db_raffle.drop_table()
# db_par.drop_table()
# db_winner.drop_table()
# db_winner_archive.drop_table()
#
# db_raffle.create_table()
# db_par.create_table()
# db_winner.create_table()
# db_winner_archive.create_table()


@dp.message(F.from_user.id.in_(admins), F.text == "/create")
async def create(msg: Message, state: FSMContext):
    await msg.answer("Введите название конкурса")
    await state.set_state(FSMAdmin_raffle.name)


@dp.message(F.from_user.id.in_(admins), StateFilter("FSMAdmin_raffle:name"))
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Выберете розыгрышь", reply_markup=prise)
    await state.set_state(FSMAdmin_raffle.type)


@dp.callback_query(F.from_user.id.in_(admins), StateFilter("FSMAdmin_raffle:type"))
async def set_type(call: CallbackQuery, state: FSMContext):
    if call.data == "prise_lc":
        await state.update_data(type="lc")
    else:
        await state.update_data(type="server")

    await call.message.edit_text("Введите приз и количество в формате:\nПриз: Кол-во\nПриз2: Кол-во")
    await state.set_state(FSMAdmin_raffle.prise)



@dp.message(F.from_user.id.in_(admins), StateFilter("FSMAdmin_raffle:prise"))
async def set_prise(msg: Message, state: FSMContext):
    try:
        text = ""
        message = msg.text.splitlines()
        for i in range(0, len(message)):
            g = message[i].split(":")
            prise = g[0]
            count = g[1]
            text += f"{prise}: {count}\n"

        await state.update_data(prise=text)
        data = await state.get_data()
        # if data["type"] == "lc":
        #     await msg.answer("Введите утешительный приз")
        #     await state.set_state(FSMAdmin_raffle.prise_loser)
    # else:
        await msg.answer("Введите id и кол-во приза:\nId: кол-во\nId2: кол-во")
        await state.set_state(FSMAdmin_raffle.prise_id)

    except:
        await msg.answer("Неправильный формат данных")


@dp.message(F.from_user.id.in_(admins), StateFilter("FSMAdmin_raffle:prise_id"))
async def set_prise_id(msg: Message, state: FSMContext):
    try:
        prise_id = ""
        prise_count = ""
        message = msg.text.splitlines()
        for i in range(0, len(message)):
            g = message[i]
            prise = g.split(":")[0]
            count = g.split(": ")[1]
            if i < len(message)-1:
                prise_id += f"{prise},"
                prise_count += f"{count},"
            else:
                prise_id += f"{prise}"
                prise_count += f"{count}"


        await state.update_data(prise_id=prise_id)
        await state.update_data(prise_count=prise_count)
        await msg.answer("Введите утешительный приз")
        await state.set_state(FSMAdmin_raffle.prise_loser)

    except:
        await msg.answer("Неправильный формат данных")


@dp.message(F.from_user.id.in_(admins), StateFilter("FSMAdmin_raffle:prise_loser"))
async def set_prise_loser(msg: Message, state: FSMContext):
    await state.update_data(prise_loser=msg.text)
    data = await state.get_data()
    # if data["type"] == "lc":
    await msg.answer("Введите id и кол-во утешительного приза")
    await state.set_state(FSMAdmin_raffle.prise_loser_id)
    # else:
    #     await msg.answer("Введите id и кол-во утешительного приза")
    #     await state.set_state(FSMAdmin_raffle.raffle)


@dp.message(F.from_user.id.in_(admins), StateFilter("FSMAdmin_raffle:prise_loser_id"))
async def set_prise_loser_id(msg: Message, state: FSMContext):
    try:
        prise_loser_id = ""
        prise_loser_count = ""
        message = msg.text.splitlines()
        for i in range(0, len(message)):
            g = message[i]
            prise = g.split(":")[0]
            count = g.split(": ")[1]
            prise_loser_id += f"{prise}"
            prise_loser_count += f"{count}"

        await state.update_data(prise_loser_id=prise_loser_id)
        await state.update_data(prise_loser_count=prise_loser_count)
        await msg.answer("Введите тело поста")
        await state.set_state(FSMAdmin_raffle.raffle)

    except:
        await msg.answer("Неправильный формат данных")


@dp.message(F.from_user.id.in_(admins), StateFilter("FSMAdmin_raffle:raffle"))
async def create_raffle(msg: Message, state: FSMContext):
    if msg.photo:
        try:
            file_id = msg.photo[3].file_id
        except:
            file_id = msg.photo[2].file_id
        resp = requests.get(f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}")
        img_path = resp.json()["result"]["file_path"]
        img = requests.get(f"https://api.telegram.org/file/bot{TOKEN}/{img_path}")
        img = Image.open(io.BytesIO(img.content))
        if not os.path.exists("static"):
            os.mkdir("static")
        img_name = secrets.token_hex(8)
        img.save(f"static/{img_name}.png", format="PNG")
        await bot.send_photo(chat_id=msg.from_user.id, photo=FSInputFile(f"static/{img_name}.png"), caption=msg.caption,
                             reply_markup=sure,
                                             parse_mode="HTML")


    if msg.video:
        file_id = msg.video.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        gg = await bot.download_file(file_path, "video.mp4")
        await bot.send_video(chat_id=msg.from_user.id, video=FSInputFile("video.mp4"), caption=msg.caption, reply_markup=sure,
                                             parse_mode="HTML")

    if msg.text:
        await bot.send_message(chat_id=msg.from_user.id, text=msg.text, reply_markup=sure,
                                             parse_mode="HTML")
    await state.set_state(FSMAdmin_raffle.sure)


@dp.callback_query(F.from_user.id.in_(admins), StateFilter("FSMAdmin_raffle:sure"))
async def sure_raffle(call: CallbackQuery, state: FSMContext):
    if call.data == "raffle_sure":
        post = 0
        # post = await bot.copy_message(chat_id=chanel, from_chat_id=call.from_user.id, message_id=call.message.message_id)
        if call.message.photo:
            post = await bot.send_photo(chat_id=chanel, photo=call.message.photo[0].file_id, caption=call.message.caption, reply_markup=add_user(user_id=call.from_user.id, msg_id=call.message.message_id))

        if call.message.video:
            post = await bot.send_video(chat_id=chanel, video=call.message.video[0].file_id, caption=call.message.caption, reply_markup=add_user(user_id=call.from_user.id, msg_id=call.message.message_id))

        if call.message.text:
            post = await bot.send_message(chat_id=chanel, text=call.message.text, reply_markup=add_user(user_id=call.from_user.id, msg_id=call.message.message_id))

        pr = await state.get_data()
        prises = ""
        counts = ""
        for i in range(0, len(pr["prise"].splitlines())):
            if i < len(pr["prise"].splitlines())-1:
                prises += f'{pr["prise"].splitlines()[i].split(":")[0]},'
                counts += f'{pr["prise"].splitlines()[i].split(":  ")[1]},'
            else:
                prises += f'{pr["prise"].splitlines()[i].split(":")[0]}'
                counts += f'{pr["prise"].splitlines()[i].split(":  ")[1]}'
        db_raffle.add_user(msg_id=post.message_id, name=pr["name"], type=pr["type"], prise=prises, count=counts, prise_loser=pr["prise_loser"], prise_id=pr["prise_id"], prise_count=pr["prise_count"], prise_loser_id=pr["prise_loser_id"], prise_loser_count=pr["prise_loser_count"])
        await call.message.answer("Розыгрыш отравлен")

    if call.data == "raffle_cancel":
        await call.message.answer("Розыгрыш отменен")

    await state.clear()


@dp.callback_query(Raffle.filter(F.status == 0))
async def add_raffle_user(call: CallbackQuery):
    if check_sub_channel(await bot.get_chat_member(chat_id=chanel, user_id=call.from_user.id),
                                 call.from_user.id):
        try:
            if db_raffle.get_state(msg_id=call.message.message_id) == None:
                if db_par.get_user(call.from_user.id, call.message.message_id) == None:
                    if call.from_user.username != None:
                        user_name = call.from_user.username
                    else:
                        user_name = call.from_user.id
                    db_par.add_user(raffle_id=db_raffle.get_id(msg_id=call.message.message_id), user_id=call.from_user.id, msg_id=call.message.message_id, username=user_name)
                    await bot.edit_message_reply_markup(chat_id=chanel, message_id=call.message.message_id, reply_markup=add_user(user_id=call.from_user.id, msg_id=call.message.message_id))
                else:
                    await call.answer("Вы уже учавствуете")
            else:
                await call.answer("Розыгрыш завершён")
        except:
            await call.answer("Розыгрыш завершён")
    else:
        await call.answer(f"Вы не подписанны на канал @{chanel_username}")


@dp.message(F.from_user.id.in_(admins), F.text == "/adm")
async def adm(msg: Message):
    await msg.answer("Админ панель", reply_markup=raffle(db_raffle.get_count_id()))


@dp.callback_query(F.from_user.id.in_(admins), Raffle_Edit.filter(F.status == 1))
async def adm_menu(call: CallbackQuery):
   data = call.data.split(":")
   await call.message.edit_text(text=data[1], reply_markup=random_win(msg_id=data[2], id=data[3], raffle_id=data[-1]))


@dp.callback_query(F.from_user.id.in_(admins), Raffle_Choose.filter(F.status == 2))
async def adm_menu_select(call: CallbackQuery):
    data = call.data.split(":")
    if data[4] == "choose":
        # try:
        sub = True
        try:
            prises = db_raffle.get_prise(data[3]).split(',')
            counts = db_raffle.get_count(data[3]).split(',')
            prise_id = db_raffle.get_prise_id(data[3]).split(',')
            prise_count = db_raffle.get_prise_count(data[3]).split(',')
            winner_count = db_par.get_max_id_us(data[2])
            winners = ""
            win_list = []
            for i in range(0, len(counts)):
                for _ in range(0, int(counts[i])):
                    while sub:
                        random_winner = random.randint(1, int(winner_count))
                        random_winner = db_par.get_winner(id=int(random_winner), msg_id=int(data[2]))
                        if check_sub_channel(await bot.get_chat_member(chat_id=chanel, user_id=int(random_winner)),
                                             call.from_user.id) and int(random_winner) not in win_list:
                            winners += f"[{db_par.get_user_name(random_winner)}](https://t.me/{db_par.get_user_name(random_winner)}) - {prises[i]} - id={prise_id[i]} - кол-во={prise_count[i]}\n"
                            win_list.append(int(random_winner))
                            break
            await call.message.answer(winners, reply_markup=confirm_buttons(msg_id=int(data[2]), id=data[3], raffle_id=db_raffle.get_id(msg_id=data[2])), parse_mode="Markdown", disable_web_page_preview=True,)

        except TypeError:
            await call.answer("Никто не учавствует")


    if data[4] == "del":
        db_raffle.del_raffle(msg_id=data[2])
        await call.message.answer("Розыгрышь удалён")

    if data[4] == "back":
        await call.message.edit_text(text="Админ панель", reply_markup=raffle(db_raffle.get_count_id()))


@dp.message(F.from_user.id.in_(admins), F.text == "/del_all")
async def dell_all(msg: Message):
    db_raffle.drop_table()
    db_par.drop_table()
    await msg.answer("Все таблицы удалены")
    db_raffle.create_table()
    db_par.create_table()


@dp.callback_query(F.data == "stop")
async def raffle_none(call: CallbackQuery):
    await call.answer("Розыгрышь завершился")


@dp.callback_query(F.from_user.id.in_(admins), Raffle_Rerol.filter(F.status == 4))
async def rerol(call: CallbackQuery):
    winners = call.message.text
    data = call.data.split(":")
    try:
        if db_raffle.get_state(msg_id=data[2]) != "end":
            if data[4] == "rerol":
                sub = True
                try:
                    prises = db_raffle.get_prise(data[3]).split(',')
                    counts = db_raffle.get_count(data[3]).split(',')
                    prise_id = db_raffle.get_prise_id(data[3]).split(',')
                    prise_count = db_raffle.get_prise_count(data[3]).split(',')
                    winner_count = db_par.get_max_id_us(data[2])
                    winners = ""
                    win_list = []
                    for i in range(0, len(counts)):
                        for _ in range(0, int(counts[i])):
                            while sub:
                                random_winner = random.randint(1, int(winner_count))
                                random_winner = db_par.get_winner(id=int(random_winner), msg_id=int(data[2]))
                                if check_sub_channel(await bot.get_chat_member(chat_id=chanel, user_id=int(random_winner)),
                                                     call.from_user.id) and int(random_winner) not in win_list:
                                    winners += f"[{db_par.get_user_name(random_winner)}](https://t.me/{db_par.get_user_name(random_winner)}) - {prises[i]} - id={prise_id[i]} - кол-во={prise_count[i]}\n"
                                    win_list.append(int(random_winner))
                                    break
                    await call.message.answer(winners, reply_markup=confirm_buttons(msg_id=int(data[2]), id=data[3],
                                                                                    raffle_id=db_raffle.get_id(
                                                                                        msg_id=data[2])),
                                              parse_mode="Markdown", disable_web_page_preview=True, )

                except TypeError:
                            await call.answer("Никто не учавствует")

            else:
                try:
                    data = call.data.split(":")
                    win_list = []
                    loser_list = []
                    win_list_user = []
                    winners = winners.splitlines()
                    winners_text = ""
                    for i in range(0, len(winners)):
                        winer = winners[i]
                        win_list.append((winer))

                    for i in win_list:
                        username = i.split(" - ")[0]
                        prise = i.split(" - ")[1]
                        user_id = db_par.get_user_id_name(username=username)
                        prise_id = i.split(" - ")[2].split("=")[1]
                        prise_count = i.split(" - ")[3].split("=")[1]
                        db_winner.add_user(user_id=user_id, msg_id=db_par.get_msg_id(user_id=user_id, raffle_id=data[5]), username=username, prise=prise, prise_id=prise_id, prise_count=prise_count)
                        db_winner.set_state(state="winner", user_id=user_id)
                        win_list_user.append(user_id)
                        winners_text += f"[{username}](https://t.me/{username}) - {prise}\n"

                    for i in range(0, db_par.get_max_id(raffle_id=data[5])+1):
                        user_id = db_par.get_user_id(id=i)
                        username = db_par.get_user_name(user_id=user_id)
                        prise = db_raffle.get_loser_prise(id=data[5])
                        prise_loser_id = db_raffle.get_prise_loser_id(id=db_par.get_msg_id(user_id=user_id, raffle_id=data[5]))
                        prise_loser_count = db_raffle.get_prise_loser_count(id=db_par.get_msg_id(user_id=user_id, raffle_id=data[5]))

                        if user_id not in win_list_user and user_id != None:
                            db_winner.add_user(user_id=user_id, msg_id=db_par.get_msg_id(user_id=user_id, raffle_id=data[5]), username=username, prise=prise, prise_id=prise_loser_id, prise_count=prise_loser_count)
                            db_winner.set_state(state="loser", user_id=user_id)
                    await bot.send_message(chat_id=chanel, text=post_text(id=data[3], winners=winners_text,
                                                                          loser_prise=db_raffle.get_loser_prise(data[3]),
                                                                          participants_count=db_par.get_max_id_us(data[2]),
                                                                          winner_count=len(winners)),
                                           parse_mode="Markdown", disable_web_page_preview=True, reply_markup=get_prise_button)
                    await call.message.answer("Розыгрышь завершён")
                    db_raffle.set_state(state="end", id=data[3])

                except:
                    await call.message.answer_dice("Розыгышь завершён")

        else:
            await call.message.answer_dice("Розыгышь завершён")

    except:
        await call.message.answer_dice("Розыгышь завершён")



@dp.message(CommandStart())
async def get_prise(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    if db_winner.get_user_exist(user_id=user_id) != None:
        if db_raffle.get_type(msg_id=db_winner.get_msg_id(user_id=user_id)) == "lc":
            await state.set_state(Set_Email.email)
            await msg.answer(win_text_lc(db_winner.get_prise(user_id=user_id)), parse_mode="Markdown")
        else:
            await state.set_state(Set_Nick.name)
            await msg.answer(
                win_text_server(db_winner.get_prise(user_id=user_id)), parse_mode="Markdown")


    else:
        await msg.answer("Добро пожаловать!\n Принимайте участие в наших конкурсах на канале @gg", reply_markup=chanel_link)


@dp.message(StateFilter("Set_Email:email"))
async def set_email(msg: Message, state: FSMContext):
    await state.update_data(email=msg.text)
    await state.set_state(Set_Email.confirm)
    await msg.answer(text=f"Внимательно проверьте введёную информацию:\nПриз: {db_winner.get_prise(user_id=msg.from_user.id)}\nEmail: {msg.text}", reply_markup=confirm)


@dp.message(StateFilter("Set_Nick:name"))
async def set_nick(msg: Message, state: FSMContext):
    await state.update_data(nick=msg.text)
    await state.set_state(Set_Nick.confirm)
    await msg.answer(text=f"Внимательно проверьте введёную информацию:\nПриз: {db_winner.get_prise(user_id=msg.from_user.id)}\nNick: {msg.text}", reply_markup=confirm)


@dp.callback_query(StateFilter("Set_Email:confirm"), F.data.startswith("confirm_"))
async def confirm_email(call: CallbackQuery, state: FSMContext):
    if call.data == "confirm_confirm":
        msg_id = db_winner.get_msg_id(user_id=call.from_user.id)
        prise = db_winner.get_prise(user_id=call.from_user.id)
        db_winner_archive.add_user(user_id=call.from_user.id, username=call.from_user.username, msg_id=msg_id, prise=prise, status="take")
        await bot.send_message(chat_id=admin, text=f"[{call.from_user.full_name}](https://t.me/{call.from_user.username})\n{call.message.text.splitlines()[1]}\n{call.message.text.splitlines()[2]}", parse_mode="Markdown", disable_web_page_preview=True)
        db_winner.del_winner(user_id=call.from_user.id)
        await call.message.edit_text("Приз выдан")
        await state.clear()
    else:
        user_id = call.from_user.id
        await state.set_state(Set_Email.email)
        if db_winner.get_user_exist(user_id=user_id) != None:
            if db_raffle.get_type(msg_id=db_winner.get_msg_id(user_id=user_id)) == "lc":
                await call.message.answer(
                    win_text_lc(db_winner.get_prise(user_id=user_id)),
                    parse_mode="Markdown")
            else:
                await state.set_state(Set_Nick.name)
                await call.message.answer(
                    win_text_server(db_winner.get_prise(user_id=user_id)),
                    parse_mode="Markdown")


@dp.callback_query(StateFilter("Set_Nick:confirm"), F.data.startswith("confirm_"))
async def confirm_nick(call: CallbackQuery, state: FSMContext):
    if call.data == "confirm_confirm":
        data = await state.get_data()
        user_id = call.from_user.id
        msg_id = db_winner.get_msg_id(user_id=user_id)
        prise = db_winner.get_prise(user_id=user_id)
        username = db_winner.get_user_name(user_id=user_id)
        db_winner_archive.add_user(user_id=user_id, username=username, msg_id=msg_id,
                                   prise=prise, status="taken")
        if db_winner.get_status(user_id=user_id, msg_id=msg_id) == "winner":
            item_id = db_raffle.get_prise_id(id=msg_id)
            count = db_raffle.get_prise_count(id=msg_id)
        else:
            item_id = db_raffle.get_prise_loser_id(id=msg_id)
            count = db_raffle.get_prise_loser_count(id=msg_id)

        db_server.give_prise(owner_id=data["nick"], item_id=item_id, count=count)
        await call.message.edit_text("Приз выдан")
        db_winner.del_winner(user_id=call.from_user.id)
        await state.clear()
    else:
        user_id = call.from_user.id
        await state.set_state(Set_Nick.name)
        if db_winner.get_user_exist(user_id=user_id) != None:
            if db_raffle.get_type(msg_id=db_winner.get_msg_id(user_id=user_id)) == "lc":
                await call.message.answer(
                    win_text_lc(db_winner.get_prise(user_id=user_id)),
                    parse_mode="Markdown")
            else:
                await state.set_state(Set_Nick.name)
                await call.message.answer(
                    win_text_server(db_winner.get_prise(user_id=user_id)),
                    parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

print(1)
if __name__ == "__main__":
    asyncio.run(main())
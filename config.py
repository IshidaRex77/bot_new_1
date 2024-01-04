import datetime

TOKEN = "6772854362:AAE1rkUUDgqNfR6jgQkWo0PpLloTtPliXOM"
admins = [6588363012]
admin = 6588363012
chanel = -1002053810315
chanel_username = "GrandReal_net"
bot_username = "Grand_Real_Bot"
site = "https://GrandReal.net"

def post_text(id, winners, loser_prise, participants_count, winner_count):
    text = f"📢 Акция от gg №{id}\n\nРозыгрыш от @{chanel_username} для наших игроков\n\nПризовые места:\n{winners}\n\n☑️Бонус за участие - {loser_prise}!\n\nУчастников: {participants_count}\nКол-во победителей: {winner_count}\nСайт проекта:{site} (https://gg.com/)\nИтоги конкурса: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')} по МСК"
    return text

def win_text_lc(prise):
    text = f"Поздравляем\n\n*Вы выиграли {prise} на Личный Кабинет*\nВведите свою почту, чтобы получить приз"
    return text

def win_text_server(prise):
    text = f"Поздравляем\n\n*Вы выиграли {prise} на сервере 1*\nВведите свой игровой никнейм, чтобы получить приз"
    return text


db_raffle = f"CREATE TABLE IF NOT EXISTS raffle(id SMALLINT, name text, type tinytext, prise text, count text, prise_id text, prise_count text, prise_loser text, prise_loser_id text, prise_loser_count text, msg_id int, state tinytext);"
db_participant = f"CREATE TABLE IF NOT EXISTS participant(id smallint, raffle_id smallint, msg_id int, user_id bigint, username text);"
db_winner = f"CREATE TABLE IF NOT EXISTS winner(id smallint, msg_id int, user_id bigint, username text, prise text, prise_id text, prise_count text, status text);"
db_winner_archive = f"CREATE TABLE IF NOT EXISTS winner_archive(id smallint, msg_id int, user_id bigint, username text, prise text, status text);"


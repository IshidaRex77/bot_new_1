
import mysql.connector
from config import db_winner


class Database_winner:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="",
            database="",
            user="",
            password=""
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def drop_table(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute("""DROP TABLE winner;""")
            print("[INFO]Table winner was deleted")

    #  создание таблицы
    def create_table(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""{db_winner};""")
            print("[INFO]Table winner created successfully")

    def add_user(self, user_id, msg_id, username, prise, prise_id, prise_count):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""Select max(id) from winner WHERE msg_id={msg_id};""")
            gg = self.cursor.fetchone()[0]
            self.connection.reconnect()
            if gg != None:
                return self.cursor.execute(F"""INSERT INTO winner (user_id, msg_id, id, prise, username, prise_id, prise_count) VALUES ({user_id}, {msg_id}, {gg+1}, '{prise}', '{username}', '{prise_id}', '{prise_count}');""")
            else:
                self.connection.reconnect()
                return self.cursor.execute(
                    F"""INSERT INTO winner (user_id, msg_id, id, prise, username, prise_id, prise_count) VALUES ({user_id}, {msg_id}, {1}, '{prise}', '{username}', '{prise_id}', '{prise_count}');""")

    def get_user_exist(self, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM winner WHERE user_id = {user_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def del_winner(self, user_id):
        with self.connection:
            self.connection.reconnect()
            return self.cursor.execute(F"""DELETE FROM winner WHERE user_id = {user_id};""")


    def get_user_id(self, user_id, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM winner WHERE user_id = {user_id} and msg_id = {msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_user_name(self, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_name FROM winner WHERE user_id = {user_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_user(self, user_id, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM winner WHERE user_id = {user_id} and msg_id = {msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_msg_id(self, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT msg_id FROM winner WHERE user_id = {user_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_user_id_random(self, id_us):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM winner WHERE id_us = {id_us};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_id(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT id FROM winner WHERE user_id = {id};""")
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_count_users(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select count(user_id) from winner WHERE msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_count_id(self):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from winner;""")
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_max_id1(self):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from winner;""")
                return self.cursor.fetchone()[0]
            except:
                return None
    def get_max_id(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from winner WHERE msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_max_id_us(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id_us) from winner WHERE msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_winner(self, id, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select user_id from winner WHERE id={id} and msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_status(self, user_id, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select status from winner WHERE user_id = {user_id} and msg_id = {msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_prise(self, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT prise FROM winner WHERE user_id = {user_id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_user_id_name(self, username):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT user_id FROM winner WHERE username = '{username}';"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def set_state(self, state, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""UPDATE winner SET state = '{state}' WHERE user_id = {user_id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

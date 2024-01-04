
import mysql.connector
from config import db_winner_archive


class Database_winner_archive:
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
            self.cursor.execute("""DROP TABLE winner_archive;""")
            print("[INFO]Table winner_archive was deleted")

    #  создание таблицы
    def create_table(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""{db_winner_archive};""")
            print("[INFO]Table winner_archive created successfully")

    def add_user(self, user_id, msg_id, username, prise, status):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""Select max(id) from winner_archive WHERE msg_id={msg_id};""")
            gg = self.cursor.fetchone()[0]
            self.connection.reconnect()
            if gg != None:
                return self.cursor.execute(F"""INSERT INTO winner_archive (user_id, msg_id, id, prise, username, status) VALUES ({user_id}, {msg_id}, {gg+1}, '{prise}', '{username}', '{status}');""")
            else:
                self.connection.reconnect()
                return self.cursor.execute(
                    F"""INSERT INTO winner_archive (user_id, msg_id, id, prise, username, status) VALUES ({user_id}, {msg_id}, {1}, '{prise}', '{username}', '{status}');""")

    def get_user_exist(self, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM winner_archive WHERE user_id = {user_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def del_winner_archive(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            return self.cursor.execute(F"""DELETE FROM winner_archive WHERE msg_id = {msg_id};""")


    def get_user_id(self, user_id, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM winner_archive WHERE user_id = {user_id} and msg_id = {msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_user_name(self, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_name FROM winner_archive WHERE user_id = {user_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_user(self, user_id, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM winner_archive WHERE user_id = {user_id} and msg_id = {msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_msg_id(self, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT msg_id FROM winner_archive WHERE user_id = {user_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_user_id_random(self, id_us):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM winner_archive WHERE id_us = {id_us};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_id(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT id FROM winner_archive WHERE user_id = {id};""")
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_count_users(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select count(user_id) from winner_archive WHERE msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_count_id(self):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from winner_archive;""")
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_max_id1(self):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from winner_archive;""")
                return self.cursor.fetchone()[0]
            except:
                return None
    def get_max_id(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from winner_archive WHERE msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_max_id_us(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id_us) from winner_archive WHERE msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_winner_archive(self, id, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select user_id from winner_archive WHERE id={id} and msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_status(self, user_id, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select status from winner_archive WHERE user_id = {user_id} and msg_id = {msg_id};""")
                print(self.cursor.fetchone())
            except:
                return None

    def get_prise(self, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT prise FROM winner_archive WHERE user_id = {user_id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_user_id_name(self, username):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT user_id FROM winner_archive WHERE username = '{username}';"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

import mysql.connector
from config import db_participant


class Database_participant:
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
            self.cursor.execute("""DROP TABLE participant;""")
            print("[INFO]Table participant was deleted")

    #  создание таблицы
    def create_table(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""{db_participant};""")
            print("[INFO]Table participant created successfully")

    def add_user(self, user_id, raffle_id, msg_id, username):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""Select max(id) from participant WHERE msg_id = {msg_id};""")
            gg = self.cursor.fetchone()[0]
            self.connection.reconnect()
            if gg != None:
                return self.cursor.execute(F"""INSERT INTO participant (user_id, raffle_id, msg_id, id, username) VALUES ({user_id}, {raffle_id}, {msg_id}, {gg+1}, '{username}');""")
            else:
                self.connection.reconnect()
                return self.cursor.execute(
                    F"""INSERT INTO participant (user_id, raffle_id, msg_id, id, username) VALUES ({user_id}, {raffle_id}, {msg_id}, {1}, '{username}');""")

    def get_user_exist(self, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM participant WHERE user_id = {user_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def del_participant(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            return self.cursor.execute(F"""DELETE FROM participant WHERE msg_id = {msg_id};""")


    def get_user_id(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM participant WHERE id = {id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_user_name(self, user_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT username FROM participant WHERE user_id = {user_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_user(self, user_id, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM participant WHERE user_id = {user_id} and msg_id = {msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_msg_id(self, user_id, raffle_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT msg_id FROM participant WHERE user_id = {user_id} and raffle_id = {raffle_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_id(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT id FROM participant WHERE user_id = {id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_count_users(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select count(user_id) from participant WHERE msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_count_id(self):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from participant;""")
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_max_id1(self):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from participant;""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_max_id(self, raffle_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from participant WHERE raffle_id={raffle_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_max_id_us(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from participant WHERE msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_winner(self, id, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select user_id from participant WHERE id={id} and msg_id={msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_user_id_name(self, username):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT user_id FROM participant WHERE username = '{username}';"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None


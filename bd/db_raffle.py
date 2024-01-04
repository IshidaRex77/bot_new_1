
import mysql.connector
from config import db_raffle


class Database_raffle:
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
            self.cursor.execute("""DROP TABLE raffle;""")
            print("[INFO]Table raffle was deleted")

    #  создание таблицы
    def create_table(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""{db_raffle};""")
            print("[INFO]Table raffle created successfully")

    def add_user(self, msg_id, name, type, prise, count, prise_id, prise_count, prise_loser, prise_loser_id, prise_loser_count):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute("""Select max(id) from raffle;""")
            gg = self.cursor.fetchone()[0]
            if gg != None:
                return self.cursor.execute(
                    f"""INSERT INTO raffle (id, msg_id, name, type, prise, count, prise_id, prise_count, prise_loser, prise_loser_id, prise_loser_count) VALUES ({gg+1}, {msg_id}, '{name}', '{type}', '{prise}', '{count}', '{prise_id}', '{prise_count}', '{prise_loser}', '{prise_loser_id}', '{prise_loser_count}');""")
            else:
                return self.cursor.execute(
                    f"""INSERT INTO raffle (id, msg_id, name, type, prise, count, prise_id, prise_count, prise_loser, prise_loser_id, prise_loser_count) VALUES (1, {msg_id}, '{name}', '{type}', '{prise}', '{count}', '{prise_id}', '{prise_count}', '{prise_loser}', '{prise_loser_id}', '{prise_loser_count}');""")

    def get_prise(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT prise FROM raffle WHERE id = {id} or msg_id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_prise_id(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT prise_id FROM raffle WHERE id = {id} or msg_id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_prise_count(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT prise_count FROM raffle WHERE id = {id} or msg_id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_prise_loser_id(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT prise_loser_id FROM raffle WHERE id = {id} or msg_id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_prise_loser_count(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT prise_loser_count FROM raffle WHERE id = {id} or msg_id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None


    def set_state(self, state, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""UPDATE raffle SET state = '{state}' WHERE id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def set_prise_id(self, prise_id, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""UPDATE raffle SET prise_id = '{prise_id}' WHERE id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def set_prise_count(self, prise_count, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""UPDATE raffle SET prise_count = '{prise_count}' WHERE id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def set_prise_loser_id(self, prise_loser_id, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""UPDATE raffle SET prise_loser_id = '{prise_loser_id}' WHERE id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def set_prise_loser_count(self, prise_loser_count, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""UPDATE raffle SET prise_loser_count = '{prise_loser_count}' WHERE id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_state(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT state from raffle WHERE msg_id = {msg_id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_count(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT count FROM raffle WHERE id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_name(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT name FROM raffle WHERE id = {id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None


    def get_id(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""SELECT id FROM raffle WHERE msg_id = {msg_id};"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_msg_id(self, name):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT msg_id FROM raffle WHERE name = '{name}';""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_type(self, msg_id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT type FROM raffle WHERE msg_id = {msg_id};""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_count_id(self):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select max(id) from raffle;""")
                return self.cursor.fetchone()[0]
            except:
                return None

    def get_loser_prise(self, id):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""Select prise_loser from raffle WHERE id = {id} or msg_id = {id};""")
                return self.cursor.fetchone()[0]
            except:
                return None


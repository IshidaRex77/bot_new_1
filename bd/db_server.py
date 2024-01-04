import mysql.connector


class Database_server:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="",
            database="",
            user="",
            password=""
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()


    def give_prise(self, owner_id, item_id, count):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(
                    f"""INSERT INTO `items_delayed` (owner_id, item_id, count) VALUES ({owner_id}, {item_id}, {count});"""
                )
                return self.cursor.fetchone()[0]
            except:
                return None
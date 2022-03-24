from multiprocessing import connection
import string
import mysql.connector 

class BotDB:

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            port="3306",
            database=db_file
        )
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute(f"SELECT id_telegramm FROM users WHERE id_telegramm = {user_id}")
        data = self.cursor.fetchone()
        if (data is None):
            return False
        return True

    def check_user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе и его статус"""
        try:
            connection = mysql.connector.connect(user='root', passwd="", port="3306", host="localhost", database=self.db_file)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE id_telegramm = {user_id}")
            result = cursor.fetchone()
            connection.close()
            return result
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    def add_user(self, user_name, user_phone, user_addr, user_id):
        """Добавляем юзера в базу"""
        try:
            sql = "INSERT INTO users (name, phone_number, lot_number, id_telegramm, approved) VALUES (%s, %s, %s, %s, 0)"
            val = (user_name, user_phone, user_addr, user_id)
            connection = mysql.connector.connect(user='root', passwd="", port="3306", host="localhost", database=self.db_file)
            cursor = connection.cursor()
            cursor.execute(sql, val)
            connection.commit()
            connection.close()
            return True
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return False

    def get_message(self, message_id: string):
        try:
            connection = mysql.connector.connect(user='root', passwd="", port="3306", host="localhost", database=self.db_file)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM messages WHERE message_id = '{message_id}'")
            result = cursor.fetchone()
            connection.close()
            return result[1]
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return None

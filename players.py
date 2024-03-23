#import mysql.connector
import sqlite3
import settings
# Параметры подключения к базе данных
config = settings.CONFIG

conn = sqlite3.connect('db_bot')
cursor = conn.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS players (
    id          INTEGER PRIMARY KEY,
    user_id     VARCHAR (255),
    user_name   VARCHAR (255),
    link        VARCHAR (255)

);
'''

cursor.execute(create_table_query)
conn.commit()

class connect():
    def add_player(user_id, user_name, link):
        try:
            conn = sqlite3.connect('db_bot')
            cursor = conn.cursor()
            insert_data_query = "INSERT INTO players (user_id, user_name, link) VALUES (?, ?, ?)"
            data = (user_id, user_name, link)#Сюда передаем аргументы
            cursor.execute(insert_data_query, data)
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    def select_users(link):
        try:
            conn = sqlite3.connect('db_bot')
            cursor = conn.cursor()
            select_data_query = f"SELECT user_name, user_id FROM players WHERE link ='{link}'"
            cursor.execute(select_data_query)
            result = cursor.fetchall()
            lst = []
            dict = {}
            for user_name, user_id in result:
                dict[user_id] = user_name
            return dict 
            """ if len(result) > 0:
                for i in result:
                    lst.append(''.join(i[0]))
            return lst """
        finally:
            cursor.close()
            conn.close()


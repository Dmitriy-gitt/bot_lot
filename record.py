#import mysql.connector
import sqlite3
import settings
# Параметры подключения к базе данных
config = settings.CONFIG


# Создание таблицы
""" create_table_query = "CREATE TABLE bot (id INT AUTO_INCREMENT PRIMARY KEY, text TEXT, data_public DATE, data_lot DATE, user VARCHAR(255), link VARCHAR(255))"
cursor = conn.cursor()
cursor.execute(create_table_query) """

conn = sqlite3.connect('db_bot')
cursor = conn.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS bot_ (
    id          INTEGER       PRIMARY KEY,
    text         TEXT,
    data_public VARCHAR (255),
    data_lot    VARCHAR (255),
    post_id     VARCHAR (255),
    link        VARCHAR (255),
    count       VARCHAR (255) CONSTRAINT [1] NOT NULL,
    photo       VARCHAR (255) 
);
'''

cursor.execute(create_table_query)
conn.commit()


class connect():
    id = 0
    def __init__(self) -> None:
            self.conn = sqlite3.connect('db_bot')
            self.cursor = self.conn.cursor()

    def close(self):
            self.cursor.close()
            self.conn.close()

    def add_date(self, date_string): 
        try:
            c = connect()
            insert_data_query = f"UPDATE bot_ SET data_public=? WHERE id={connect.id}"
            data = [date_string]
            c.cursor.execute(insert_data_query, data)
            c.conn.commit()
        finally:
            c.close()

    def select_date(self):
        try:
            c = connect()
            select_data_query = f"SELECT data_public FROM bot_ WHERE id ={connect.id}"
            c.cursor.execute(select_data_query)
            result = c.cursor.fetchall()
            c.conn.commit()
            return result[0][0]
        finally:
            c.close()

    def all_select_date(self, arg):
        try:
            c = connect()
            select_data_query = f"SELECT {arg} FROM bot_ WHERE {arg} IS NOT NULL"
            c.cursor.execute(select_data_query)
            result = c.cursor.fetchall()
            c.conn.commit()
            lst = []
            if len(result) >= 1:
                for i in result:
                        lst.append(''.join(i[0]))
                return lst
        finally:
            c.close()

    def add_table(self, text, data_lot, count):
        try:
            c = connect()
            insert_data_query = "INSERT INTO bot_ (text, data_lot, count) VALUES (?, ?, ?)"
            data = (text, data_lot, count)  # Сюда передаем аргументы
            c.cursor.execute(insert_data_query, data)
            connect.id = c.cursor.lastrowid
            c.conn.commit()  # Сохраняем изменения в базе данных
        finally:
            c.close()

    def select_table(self):
        try:
            c = connect()
            select_data_query = f"SELECT text, data_public, data_lot, count  FROM bot_ WHERE id = {connect.id}"
            c.cursor.execute(select_data_query)
            result = c.cursor.fetchall()
            c.conn.commit()
            return result
        finally:
            c.close()

    def add_post_id(self, post_id, arg):
        try:
            c = connect()
            insert_data_query = f"UPDATE bot_ SET post_id=? WHERE data_public='{arg}'"
            data = [post_id]
            c.cursor.execute(insert_data_query, data)
            c.conn.commit()
        finally:
            c.close()

    def get_write(self, arg):
        try:
            c = connect()
            select_data_query = f"SELECT text, data_lot FROM bot_ WHERE data_public ='{arg}'"
            c.cursor.execute(select_data_query)
            result = c.cursor.fetchall()
            c.conn.commit()
            if len(result) > 0:
                return result[0]
        finally:
            c.close()

    def delete_date(self, arg, arg2):
        try:
            c = connect()
            select_data_query = f"UPDATE bot_ SET {arg} = NULL WHERE {arg} ='{arg2}'"
            c.cursor.execute(select_data_query)
            c.conn.commit()
        finally:
            c.close()

    def add_link(self, arg, arg2):
        try:
            c = connect()
            select_data_query = f"UPDATE bot_ SET link ='{arg}' WHERE data_public ='{arg2}'"
            c.cursor.execute(select_data_query)
            c.conn.commit()
        finally:
            c.close()

    def get_link(self, arg):
        try:
            c = connect()
            select_data_query = f"SELECT link, count FROM bot_ WHERE data_lot ='{arg}'"
            c.cursor.execute(select_data_query)
            result = c.cursor.fetchall()
            c.conn.commit()
            lst = []
            if len(result) > 0:
                for i in result:
                    for k in i:
                        lst.append(k)
                    return (lst)
        finally:
            c.close()

    def get_post_id(self, arg):
        try:
            c = connect()
            select_data_query = f"SELECT post_id FROM bot_ WHERE data_lot ='{arg}'"
            c.cursor.execute(select_data_query)
            result = c.cursor.fetchall()
            c.conn.commit()
            lst = []
            for i in result:
                for k in i:
                    lst.append(k)
            return ''.join(lst)
        finally:
            c.close()

    def add_photo(self, arg, arg2):
        try:
            c = connect()
            select_data_query = f"UPDATE bot_ SET photo ='{arg}' WHERE data_lot ='{arg2}'"
            c.cursor.execute(select_data_query)
            c.conn.commit()
        finally:
            c.close()

    def get_photo(self, arg, arg2):
        try:
            c = connect()
            select_data_query = f"SELECT photo FROM bot_ WHERE {arg} ='{arg2}'"
            c.cursor.execute(select_data_query)
            result = c.cursor.fetchall()
            c.conn.commit()
            lst = []
            for i in result:
                for k in i:
                    lst.append(k)
                return (''.join(lst))
        finally:
            c.close()

    def get_all_link(self):
        try:
            c = connect()
            select_data_query = f"SELECT link, text FROM bot_"
            c.cursor.execute(select_data_query)
            result = c.cursor.fetchall()
            c.conn.commit()
            """ lst = []
            for i in result:
                lst.append(''.join(i)) """
            return result
        finally:
            c.close()

import math
import time
import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addPost(self, title, text):
        try:
            tm = time.localtime(time.time())
            ti_me = f'{tm.tm_mday}.{tm.tm_mon}.{tm.tm_year}'
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?)", (title, text, ti_me))
            self.__db.commit()
        except sqlite3.Erorr as e:
            print('Ошибка добавление поста' + str(e))
            return False
        return True

    def getPosts(self):
        try:
            self.__cur.execute(f'SELECT id, title, text, time FROM posts ORDER BY id DESC')
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print('Ошибка получения записи' + str(e))
        return []
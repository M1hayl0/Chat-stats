import sqlite3
from sqlite3 import Error


def connect(chat):
    try:
        conn = sqlite3.connect(f"Input/{chat}.db")
        return conn
    except Error as e:
        print(e)


def disconnect(conn):
    try:
        conn.close()
    except sqlite3.Error as e:
        print(e)


def createTable(database):
    sql = """
        CREATE TABLE Messages (
            IdMes INTEGER PRIMARY KEY AUTOINCREMENT,
            month VARCHAR(2) NOT NULL,
            day VARCHAR(2) NOT NULL,
            year VARCHAR(4) NOT NULL,
            hour VARCHAR(2) NOT NULL,
            minute VARCHAR(2) NOT NULL,
            AMPM VARCHAR(2) NOT NULL,
            person VARCHAR(100) NOT NULL,
            message VARCHAR(10000) NOT NULL
        )
    """

    try:
        cursor = database.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)


def insertMessage(database, month, day, year, hour, minute, AMPM, person, message):
    sql = """
        INSERT INTO Messages(month, day, year, hour, minute, AMPM, person, message)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
    """

    try:
        with database:
            cursor = database.cursor()
            cursor.execute(sql, (month, day, year, hour, minute, AMPM, person, message))
    except sqlite3.Error as e:
        print(e)


def selectAllMessages(database):
    sql = "SELECT * FROM Messages"
    try:
        cursor = database.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(e)


def selectLastMessage(database):
    sql = "SELECT * FROM Messages ORDER BY IdMes DESC LIMIT 1"
    try:
        cursor = database.cursor()
        cursor.execute(sql)
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(e)


def selectLastMessageText(database):
    sql = "SELECT message FROM Messages ORDER BY IdMes DESC LIMIT 1"
    try:
        cursor = database.cursor()
        cursor.execute(sql)
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(e)


def updateLastMessage(database, message):
    sql = "UPDATE Messages SET message = ? WHERE IdMes = (SELECT IdMes FROM Messages ORDER BY IdMes DESC LIMIT 1)"
    try:
        with database:
            cursor = database.cursor()
            cursor.execute(sql, (message, ))
    except sqlite3.Error as e:
        print(e)


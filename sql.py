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
            year VARCHAR(2) NOT NULL,
            hour VARCHAR(2) NOT NULL,
            minute VARCHAR(2) NOT NULL,
            AMPM VARCHAR(2) NOT NULL,
            person VARCHAR(100) NOT NULL,
            message VARCHAR(10000) NOT NULL,
            app VARCHAR(10) NOT NULL
        )
    """

    try:
        cursor = database.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)


def insertMessage(database, month, day, year, hour, minute, AMPM, person, message, app):
    sql = """
        INSERT INTO Messages(month, day, year, hour, minute, AMPM, person, message, app)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    try:
        with database:
            cursor = database.cursor()
            cursor.execute(sql, (month, day, year, hour, minute, AMPM, person, message, app))
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


def selectLastMessage(database, app):
    sql = "SELECT * FROM Messages WHERE app = ? ORDER BY IdMes DESC LIMIT 1"
    try:
        cursor = database.cursor()
        cursor.execute(sql, (app, ))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(e)


def selectLastMessageText(database, app):
    sql = "SELECT message FROM Messages WHERE app = ? ORDER BY IdMes DESC LIMIT 1"
    try:
        cursor = database.cursor()
        cursor.execute(sql, (app, ))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(e)


def updateLastMessage(database, message, app):
    sql = "UPDATE Messages SET message = ? WHERE IdMes = (SELECT IdMes FROM Messages WHERE app = ? ORDER BY IdMes DESC LIMIT 1)"
    try:
        with database:
            cursor = database.cursor()
            cursor.execute(sql, (message, app))
    except sqlite3.Error as e:
        print(e)


def getAllPersons(database):
    sql = "SELECT DISTINCT person FROM Messages"
    try:
        with database:
            cursor = database.cursor()
            cursor.execute(sql)
            persons = cursor.fetchall()
            return [person[0] for person in persons]
    except sqlite3.Error as e:
        print(e)
        return []


def updatePersonName(database, newName, oldName):
    sql = "UPDATE Messages SET person = ? WHERE person = ?"
    try:
        with database:
            cursor = database.cursor()
            cursor.execute(sql, (newName, oldName))
    except sqlite3.Error as e:
        print(e)

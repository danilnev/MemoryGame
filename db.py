import sqlite3
from classes import User


# в файле описаны функции по работе с базой данных


def is_register(username, email):  # функция на проверку регистрации пользователя
    connection = sqlite3.connect('MemoryGameDatabase.db')
    cursor = connection.cursor()
    search_for_username = cursor.execute(
        '''SELECT * FROM players WHERE players.username == "{}"'''.format(username)
    ).fetchall()
    search_for_email = cursor.execute(
        '''SELECT * FROM players WHERE players.email == "{}"'''.format(email)
    ).fetchall()
    cursor.close()
    connection.close()
    if len(search_for_username) != 0:
        print(1)
        return True, 'Данный никнейм уже зарегестрирован!'
    if len(search_for_email) != 0:
        print(2)
        return True, 'Данный адрес электронной почты уже зарегестрирован!'
    print(3)
    return tuple([False])


def register(username, age, email, password):  # функция регистрирует пользователя в базе данных и возвращает User
    connection = sqlite3.connect('MemoryGameDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO players (username, age, email, password)
    VALUES (?, ?, ?, ?)''', (username, age, email, password))
    connection.commit()
    cursor.close()
    connection.close()
    return User(username, age, email, password)


def update_record(username, new_record):  # функция обновляет рекорд в базе данных
    connection = sqlite3.connect('MemoryGameDatabase.db')
    cursor = connection.cursor()
    print(username, new_record)
    cursor.execute(f'''
    UPDATE players SET record = {new_record}
    WHERE players.username == '{username}' AND (players.record < {new_record} OR players.record IS NULL)
    ''')
    connection.commit()
    cursor.close()
    connection.close()


def login(email, password):  # функция ищет пользователя для входа
    connection = sqlite3.connect('MemoryGameDatabase.db')
    cursor = connection.cursor()
    result = cursor.execute(f'''
    SELECT * FROM players WHERE players.email == ? AND players.password == ?''', (email, password)).fetchall()
    cursor.close()
    connection.close()
    if len(result) == 0:
        return False
    return User(result[0][1], result[0][2], result[0][4], result[0][5], result[0][3])


def get_records():  # функция возвращает таблицу с рекордами
    connection = sqlite3.connect('MemoryGameDatabase.db')
    cursor = connection.cursor()
    result = cursor.execute('''SELECT username, age, record FROM players''').fetchall()
    result.sort(key=lambda x: x[2] if x[2] is not None else 0, reverse=True)
    return result[:100]


def get_user_record(username):  # функция возвращает рекорд определенного пользователя
    connection = sqlite3.connect('MemoryGameDatabase.db')
    cursor = connection.cursor()
    result = cursor.execute(
        f'''SELECT username, age, record FROM players WHERE players.username == ?''', (username)
    ).fetchall()
    return result
import db


class User:  # класс пользователя
    def __init__(self, username, age, email, password, record=0):
        self.username = username
        self.age = age
        self.email = email
        self.password = password
        self.record = record

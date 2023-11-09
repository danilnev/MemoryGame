import re


def check_username(username):
    return re.match('^[a-zA-Z0-9_-]*$', username) is not None and len(username) > 2


def check_email(email):
    pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


def password_check(password):
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[-_!])[A-Za-z0-9-_!]*$', password) is not None:
        return False, 'Некорректный пароль!\n' \
                      'Он должен содержать латинские буквы,\nцифры, знаки -, _, !.'
    if len(password) < 8:
        return False, 'Некорректный пароль!\nДлина не должна быть меньше 8 символов.'
    return tuple([True])


def all_check(username, age, email, password):
    username_check_result = check_username(username)
    if not username_check_result:
        return False,\
            'Некорректное имя пользователя!\nОно должно содержать более 2 символов\n(латинские буквы, цифры, знаки -, _.)'
    if not (age.isdigit() and 0 < int(age) < 120):
        return False, 'Некорректный возраст!\nОн должен быть от 1 до 120 лет'
    email_check_result = check_email(email)
    if not email_check_result:
        return False, 'Некорректный адрес электронной почты!'
    password_check_result = password_check(password)
    if not password_check_result[0]:
        return False, password_check_result[1]
    return tuple([True])

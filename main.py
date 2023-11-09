from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QFormLayout, QWidget, \
    QVBoxLayout, QDialog, QLCDNumber, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
import sys
from check_to_correct_data import all_check
import db
import random


class MemoryGame(QMainWindow):  # основное окно с меню и игрой
    def __init__(self, user=False):
        super().__init__()
        self.user = user
        self.createUI()

    def createUI(self):  # создание интерфейса
        self.setGeometry(0, 0, 1250, 800)

        # таймер для управления задержками при игре
        self.timer = QTimer()
        self.timer.timeout.connect(self.play)

        self.name_label = QLabel(self) if self.user else None
        if self.name_label is not None:
            self.name_label.setText(self.user.username)
            self.name_label.move(900, 350)

        # настройка шрифтов
        font_for_title_id = QFontDatabase.addApplicationFont('static/fonts/font_for_title.ttf')
        font_for_title = QFontDatabase.applicationFontFamilies(font_for_title_id)
        font_for_title = QFont(font_for_title[0])
        font_for_title.setPointSize(80)

        font_for_text_id = QFontDatabase.addApplicationFont('static/fonts/minecraft.ttf')
        font_for_text = QFontDatabase.applicationFontFamilies(font_for_text_id)
        font_for_text = QFont(font_for_text[0])
        font_for_text.setPointSize(14)

        font_for_edit_id = QFontDatabase.addApplicationFont('static/fonts/arial_bolditalicmt.ttf')
        font_for_edit = QFontDatabase.applicationFontFamilies(font_for_edit_id)
        font_for_edit = QFont(font_for_edit[0])
        font_for_edit.setPointSize(14)

        self.setFont(font_for_text)

        crds_title = (self.width() - 750) // 2, 20

        # создание и управление местоположением элементов
        self.title = QLabel(self)
        self.title.setText('Memory Game')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(font_for_title)
        self.title.setFixedSize(750, 200)
        self.title.move(*crds_title)

        if self.user:
            self.record_lable = QLabel(self)
            self.record_lable.setText('Рекорд:')
            self.record_lable.setFixedSize(150, 50)
            self.record_lable.move(900, 390)

            self.record_lcd = QLCDNumber(self)
            self.record_lcd.display(str(self.user.record))
            self.record_lcd.move(1000, 400)

        self.layout_for_buttons = QVBoxLayout(self)

        self.button_play = QPushButton(self)
        self.button_play.setText('Играть')
        self.button_play.clicked.connect(self.play)

        self.button_to_register_or_login = QPushButton(self)
        self.button_to_register_or_login.setText('Зарегистрироваться / Войти')
        self.button_to_register_or_login.clicked.connect(self.register_or_login)

        self.button_records = QPushButton(self)
        self.button_records.setText('Рейтинг')
        self.button_records.clicked.connect(self.show_records)

        self.button_stastic = QPushButton(self)
        self.button_stastic.setText('Возрастная статистика')
        self.button_stastic.clicked.connect(self.show_age_statistic)
        self.button_stastic.setEnabled(False)

        # собрание кнопок меню в layout
        for btn in [self.button_play, self.button_records, self.button_to_register_or_login, self.button_stastic]:
            btn.setFixedSize(500, 100)
            self.layout_for_buttons.addWidget(btn)

        self.central_widget_with_menu = QWidget()
        self.central_widget_with_menu.setLayout(self.layout_for_buttons)
        self.setCentralWidget(self.central_widget_with_menu)
        self.layout_for_buttons.setAlignment(Qt.AlignCenter)

        self.music_label = QLabel(self)
        self.music_label.setText('Музыка')

        self.music_label.setFixedSize(200, 50)
        self.music_label.setAlignment(Qt.AlignCenter)
        self.music_label.move(525, 650)

        self.music_buttons = []

        self.music_buttons.append(QPushButton(self))
        self.music_buttons[0].setText('1')
        self.music_buttons[0].clicked.connect(self.music)
        self.music_buttons[0].setFixedSize(150, 50)
        self.music_buttons[0].move(250, 700)

        self.music_buttons.append(QPushButton(self))
        self.music_buttons[1].setText('2')
        self.music_buttons[1].clicked.connect(self.music)
        self.music_buttons[1].setFixedSize(150, 50)
        self.music_buttons[1].move(450, 700)

        self.music_buttons.append(QPushButton(self))
        self.music_buttons[2].setText('3')
        self.music_buttons[2].clicked.connect(self.music)
        self.music_buttons[2].setFixedSize(150, 50)
        self.music_buttons[2].move(650, 700)

        self.music_buttons.append(QPushButton(self))
        self.music_buttons[3].setText('4')
        self.music_buttons[3].clicked.connect(self.music)
        self.music_buttons[3].setFixedSize(150, 50)
        self.music_buttons[3].move(850, 700)

        for btn in self.music_buttons:
            btn.setEnabled(False)

        # настройка кнопок для игры (на данном моменте они скрываются)
        self.now_record_label = QLabel(self)
        self.now_record_label.setText('Счет:')
        self.now_record_label.setFixedSize(150, 50)
        self.now_record_label.move(500, 225)
        self.now_record_label.hide()

        self.now_record_lcd = QLCDNumber(self)
        self.now_record_lcd.move(650, 235)
        self.now_record_lcd.hide()

        self.game_field = []
        self.game_buttons = []

        self.home_button = QPushButton('Выход', self)
        self.home_button.setStyleSheet("background-color: transparent; border: 2px solid #000; border-radius: 20px;")
        self.home_button.setGeometry(0, 0, 100, 50)
        self.home_button.move(900, 550)
        self.home_button.clicked.connect(self.home)
        self.home_button.hide()

        self.back_button = QPushButton('Заново', self)
        self.back_button.setStyleSheet("background-color: transparent; border: 2px solid #000; border-radius: 20px;")
        self.back_button.setGeometry(0, 0, 100, 50)
        self.back_button.move(900, 400)
        self.back_button.clicked.connect(self.reset_game)
        self.back_button.hide()

        self.round_number = 1
        self.buttons_to_light = 1
        self.current_sequence = []
        self.user_sequence = []
        self.colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255), (128, 0, 128), (255, 255, 0),
            (0, 128, 0)
        ]

        for i in range(3):
            self.game_field.append([])
            for j in range(3):
                btn = QPushButton(self)
                btn.setFixedSize(100, 100)
                x, y = 425 + (100 * j) + (50 * j), 300 + (100 * i) + (50 * i)
                btn.move(x, y)
                btn.hide()
                self.game_field[i].append(btn)
                self.game_buttons.append(btn)

    def play(self):  # начальная стадия игры, подготовка
        # показываем и скрываем нужные элементы
        self.central_widget_with_menu.hide()
        self.music_label.hide()
        self.name_label.hide()
        self.record_lable.hide()
        self.record_lcd.hide()
        for btn in self.music_buttons:
            btn.hide()
        self.home_button.show()
        self.back_button.show()
        self.now_record_label.show()
        self.now_record_lcd.show()
        for row in self.game_field:
            for btn in row:
                btn.show()
                btn.setEnabled(False)

        # начало игры
        self.now_record_lcd.display(str(self.round_number - 1))
        self.generate_sequence()
        self.flash_current_sequence()

    def generate_sequence(self):  # генерация последовательности кнопок на данный раунд
        if self.buttons_to_light > 1:
            new_sequence = random.choice(self.game_buttons)
            while new_sequence == self.current_sequence[-1]:
                new_sequence = random.choice(self.game_buttons)
            self.colors.append(random.choice(self.colors))
            self.current_sequence.append(new_sequence)
        else:
            self.current_sequence = [random.choice(self.game_buttons)]

    def flash_current_sequence(self):  # управление задержкой при подсвечивании последовательности
        for i, button in enumerate(self.current_sequence):
            QTimer.singleShot((i + 1) * 750, lambda btn=button: self.flash_button(btn))
        QTimer.singleShot((len(self.current_sequence) + 1) * 750, self.enable_button_clicks)

    def flash_button(self, button):  # подсвечивание последовательность
        rgb_color = self.colors[self.current_sequence.index(button)]
        button.setStyleSheet(f'background: rgb{rgb_color};')
        QTimer.singleShot(750, lambda btn=button: btn.setStyleSheet(''))

    def enable_button_clicks(self):  # установка сканирования пользовательской последовательности
        for btn in self.game_buttons:
            btn.setEnabled(True)
            btn.clicked.connect(self.on_button_click)
        self.user_sequence = []

    @pyqtSlot()
    def on_button_click(self):  # чтение нажатий пользователя и проверка на совпадение со сгенерированной
        sender = self.sender()
        if len(self.user_sequence) == 0 or sender != self.user_sequence[-1]:
            self.user_sequence.append(sender)
        self.now_record_lcd.display(self.round_number - 1)

        if len(self.user_sequence) == self.buttons_to_light:
            if self.user_sequence == self.current_sequence:
                if self.buttons_to_light < len(self.game_buttons):
                    self.user_sequence = []
                    self.buttons_to_light += 1
                    self.round_number += 1
                    self.play()
                else:
                    self.game_over()
                    return
            else:
                self.game_over()
                return

    def reset_game(self):  # перезагрузка игры
        self.game_over(False)
        self.play()

    def game_over(self, with_result=True):  # окончание игры (действие с результатом)
        record = self.round_number - 1
        if with_result:
            self.record_window = ResultWindow(record)
            self.record_window.setModal(True)
            self.record_window.exec_()
        self.round_number = 1
        self.buttons_to_light = 1
        self.current_sequence = []
        self.user_sequence = []
        if self.user:
            if record > self.user.record:
                self.user.record = record
                self.record_lcd.display(str(record))
            db.update_record(self.user.username, record)

    def register_or_login(self):  # запуск окна регистрации\входа
        self.close()
        self.registration_window = MemoryGameRegistration()
        self.registration_window.show()

    def show_records(self):  # запуск таблицы рекордов
        self.close()
        self.records_window = MemoryGameRecords(self.user)
        self.records_window.show()

    def music(self):  # функция, запускающая музыку при игре
        pass

    def home(self):  # возврат от режима игры в меню
        self.game_over(False)
        self.central_widget_with_menu.show()
        self.music_label.show()
        for btn in self.music_buttons:
            btn.show()

        self.home_button.hide()
        self.back_button.hide()
        self.now_record_label.hide()
        self.now_record_lcd.hide()
        for row in self.game_field:
            for btn in row:
                btn.hide()

    def show_age_statistic(self):  # показ статистики рекордов по возрастам
        pass


class MemoryGameRegistration(QMainWindow):  # окно регистрации и входа
    def __init__(self):
        super().__init__()
        self.createUI()

    def createUI(self):  # генерация интерфейса
        self.setGeometry(0, 0, 1250, 500)

        # настройка шрифтов
        font_for_title_id = QFontDatabase.addApplicationFont('static/fonts/font_for_title.ttf')
        font_for_title = QFontDatabase.applicationFontFamilies(font_for_title_id)
        font_for_title = QFont(font_for_title[0])
        font_for_title.setPointSize(80)

        font_for_text_id = QFontDatabase.addApplicationFont('static/fonts/minecraft.ttf')
        font_for_text = QFontDatabase.applicationFontFamilies(font_for_text_id)
        font_for_text = QFont(font_for_text[0])
        font_for_text.setPointSize(14)

        font_for_edit_id = QFontDatabase.addApplicationFont('static/fonts/arial_bolditalicmt.ttf')
        font_for_edit = QFontDatabase.applicationFontFamilies(font_for_edit_id)
        font_for_edit = QFont(font_for_edit[0])
        font_for_edit.setPointSize(20)

        self.setFont(font_for_text)

        # создание формы
        self.form_widget = QWidget()
        self.form_layout = QFormLayout(self.form_widget)
        self.layout = QVBoxLayout()

        self.title = QLabel(self)
        self.title.setText('Memory Game')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(font_for_title)

        self.login_label = QLabel('Для входа достаточно ввести почту и пароль!', self)
        self.login_label.setAlignment(Qt.AlignCenter)

        self.username_label = QLabel(self)
        self.username_label.setText('Имя пользователя:')
        self.username_field = QLineEdit(self)
        self.username_field.setFont(font_for_edit)

        self.age_label = QLabel(self)
        self.age_label.setText('Возраст:')
        self.age_field = QLineEdit(self)
        self.age_field.setFont(font_for_edit)

        self.email_label = QLabel(self)
        self.email_label.setText('Адрес электронной почты:')
        self.email_field = QLineEdit(self)
        self.email_field.setFont(font_for_edit)

        self.password_label = QLabel(self)
        self.password_label.setText('Пароль:')
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setFont(font_for_edit)

        self.register_button = QPushButton('Зарегистрироваться')
        self.register_button.clicked.connect(self.register)

        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.login)

        # генерация расположения кнопок
        self.form_layout.addRow(self.username_label, self.username_field)
        self.form_layout.addRow(self.age_label, self.age_field)
        self.form_layout.addRow(self.email_label, self.email_field)
        self.form_layout.addRow(self.password_label, self.password_field)
        self.form_layout.addRow(self.register_button)
        self.form_layout.addRow(self.login_button)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.form_widget)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def register(self):  # функция запускается кнопкой 'зарегистрироваться' и регистрирует пользователя в базе данных
        username = self.username_field.text()
        age = self.age_field.text()
        email = self.email_field.text()
        password = self.password_field.text()
        result = all_check(username, age, email, password)
        if result[0]:
            is_register = db.is_register(username, email)
            if is_register[0]:
                error_window = ErrorWindow(is_register[1])
                error_window.setModal(True)
                error_window.exec_()
                return
            else:
                user = db.register(username, age, email, password)
                self.close()
                self.memory_game_window = MemoryGame(user)
                self.memory_game_window.show()
        else:
            error_window = ErrorWindow(result[1])
            error_window.setModal(True)
            error_window.exec_()

    def login(self):  # функция запускается кнопкой 'войти' и берет пользователя из базы данных
        email = self.email_field.text()
        password = self.password_field.text()
        user = db.login(email, password)
        if user:
            self.close()
            self.memory_game_window = MemoryGame(user)
            self.memory_game_window.show()
        else:
            error_window = ErrorWindow('Пользователя не существует или пароль неверный!')
            error_window.setModal(True)
            error_window.exec_()


class MemoryGameRecords(QMainWindow):  # окно для вывода таблицы рекордов
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.createUI()

    def createUI(self):
        self.setGeometry(0, 0, 800, 800)

        # взятие таблицы из базы данных
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(0, 0, 800, 700)
        self.table_widget.setColumnCount(3)
        self.table_widget.setRowCount(0)
        self.table_widget.setHorizontalHeaderLabels(["Имя", "Возраст", "Рекорд"])

        records = db.get_records()

        # расстановка данных
        for i, row in enumerate(records):
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            for j, el in enumerate(row):
                item = QTableWidgetItem(str(el))
                item.setFlags(Qt.ItemIsEditable)
                self.table_widget.setItem(i, j, item)

        self.button_home = QPushButton(self)
        self.button_home.setText('Назад')
        self.button_home.setGeometry(0, 0, 700, 70)
        self.button_home.move(50, 715)

        # if self.user:
        #     print(self.user.username)
        #     self.table_widget_for_user = QTableWidget(self)
        #     self.table_widget_for_user.setGeometry(0, 0, 800, 100)
        #     self.table_widget_for_user.move(0, 700)
        #     self.table_widget_for_user.setRowCount(1)
        #     self.table_widget_for_user.setColumnCount(3)
        #
        #     user_record = db.get_user_record(self.user.username)
        #     for i, el in enumerate(user_record):
        #         item = QTableWidgetItem(str(el))
        #         item.setFlags(Qt.ItemIsEditable)
        #         self.table_widget_for_user.setItem(0, i, item)


class ErrorWindow(QDialog):  # окно, всплывающее при ошибке регистрации\входе
    def __init__(self, error_message):
        super().__init__()
        self.setWindowTitle('Error!')
        self.setFixedSize(400, 100)
        self.error_title = QLabel(self)
        self.error_title.setText(error_message)
        self.error_title.setFixedSize(300, 50)
        self.error_title.move(50, 0)
        self.error_title.setAlignment(Qt.AlignCenter)
        self.ok_button = QPushButton(self)
        self.ok_button.setText('OK')
        self.ok_button.move(155, 60)
        self.ok_button.clicked.connect(self.close)


class ResultWindow(QDialog):  # окно, всплывающее при окончании игры, выводит результат
    def __init__(self, record):
        super().__init__()
        self.setGeometry(0, 0, 200, 100)
        self.setWindowTitle('Игра закончена')
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self)
        self.result_label = QLabel(self)
        self.result_label.setText(f'Игра закончена. Ваш результат: {record}')
        self.btn_ok = QPushButton(self)
        self.btn_ok.setText('OK')
        self.btn_ok.clicked.connect(self.close)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.btn_ok)
        self.central_widget.setLayout(self.layout)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    memory_game = MemoryGame(False)

    memory_game.show()

    sys.excepthook = except_hook
    sys.exit(app.exec())

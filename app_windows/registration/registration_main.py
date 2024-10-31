import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog

from app_windows.registration.registration_failed import RegistrationFailed
from database import create_tables
from database.models import AppUser, AppUserConfig


class RegistrationMain(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('reg_page_template.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.check_button_signals()

    def check_button_signals(self):
        self.enter_button.clicked.connect(self.check_user_data)
        self.reg_button.clicked.connect(self.registrate_new_user)

    @property
    def users_with_same_login(self):
        login = self.login_field.text().strip()
        users_with_this_login = AppUserConfig.select().where(AppUserConfig.login == login)

        if len(users_with_this_login) == 0:
            return None

        return users_with_this_login[0].user

    def check_user_data(self):
        if not self.users_with_same_login:
            self.show_reg_failed_window(error_message="Неверный логин!")
            return

        if self.users_with_same_login.config[0].password != self.password_filed.text().strip():
            self.show_reg_failed_window(error_message="Неверный пароль!")
            return

        return 3  # Все проверки пройдены

    def registrate_new_user(self):
        if self.users_with_same_login:
            self.show_reg_failed_window(error_message=f"Логин {self.login_field.text().strip()} уже занят!")
            return  # логин уже занят

        AppUserConfig.create(
            login=self.login_field.text().strip(),
            password=self.password_filed.text().strip(),
            yandex_api_key="<no_key>",
            user=AppUser.create()
        )

        return 3  # Аккаунт создан, все проверки пройдены

    @staticmethod
    def show_reg_failed_window(error_message: str):
        ex_ = RegistrationFailed(error_message=error_message)
        ex_.exec()


# Для тестов
if __name__ == '__main__':
    create_tables()
    app = QApplication(sys.argv)
    ex = RegistrationMain()
    ex.show()
    sys.exit(app.exec())

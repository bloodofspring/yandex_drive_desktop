from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from app_windows.registration.registration_failed import WrongRegDataDialog, LoginIsTakenDialog
from config import TEMPLATES_PATH
from database.models import AppUser, AppUserConfig, Session


class RegistrationDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}reg_page_template_dialog.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.check_button_signals()

    def check_button_signals(self):
        self.enter_button.clicked.connect(self.check_user_data)
        self.reg_button.clicked.connect(self.registrate_new_user)

    # @property
    def users_with_same_login(self) -> AppUser | None:
        login = self.login_field.text().strip()
        users_with_this_login = AppUser.select().where(AppUser.login == login)[:]

        if not users_with_this_login:
            return None

        return users_with_this_login[0]

    def check_user_data(self):
        if self.users_with_same_login() is None:
            WrongRegDataDialog().exec()
            return

        if self.users_with_same_login().config.password != self.password_filed.text().strip():
            WrongRegDataDialog().exec()
            return

        Session.create(user=AppUser.get(login=self.login_field.text().strip()))

        self.close()

    def registrate_new_user(self):
        if self.users_with_same_login() is not None:
            LoginIsTakenDialog().exec()
            return  # логин уже занят

        config = AppUserConfig.create(
            password=self.password_filed.text().strip(),
            yandex_api_key="<no_key>",
        )
        app_user = AppUser.create(login=self.login_field.text().strip(), config=config)
        Session.create(user=app_user)

        self.close()

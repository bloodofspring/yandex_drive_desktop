from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from app_windows.change_loginpas_form.change_process_failed import LoginIsTakenDialog
from app_windows.change_loginpas_form.data_updated import DataSuccessfullyUpdated
from config import TEMPLATES_PATH
from database.models import AppUser, AppUserConfig
from util import get_last_session


class GetAuthTokenDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}change_loginpas_form.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.check_button_signals()

    def check_button_signals(self):
        self.save_btn.clicked.connect(self.check_and_save_data)
        self.cancel_button.clicked.connect(self.close)

    def users_with_same_login(self) -> AppUser | None:
        login = self.login_field.text().strip()
        users_with_this_login = AppUser.select().where(AppUser.login == login)[:]

        if not users_with_this_login:
            return None

        return users_with_this_login[0]

    def check_and_save_data(self):
        if self.users_with_same_login() is not None:
            LoginIsTakenDialog().exec()
            return  # логин уже занят

        latest_session = get_last_session(show_alert=False)
        if latest_session is None:
            return

        user = latest_session.user
        config = user.config

        config.password = self.password_field.text().strip()
        user.login = self.login_field.text().strip()

        AppUser.save(user)
        AppUserConfig.save(config)

        DataSuccessfullyUpdated().exec()

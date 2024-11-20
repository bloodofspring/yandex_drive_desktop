from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from yadisk import YaDisk

from app_windows.change_token_form.not_implemented_yet import AddLater
from app_windows.dialog_samples import EmptyDialog
from config import TEMPLATES_PATH
from database.models import AppUser, AppUserConfig
from util import get_last_session


class WrongTokenDialog(EmptyDialog):
    INFO = "Указан неверный токен!"


class ChangeAuthTokenDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}change_token_form.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.check_button_signals()

    def check_button_signals(self):
        self.save_btn.clicked.connect(self.check_and_save)
        self.cancel_btn.clicked.connect(self.close)
        self.instruction_button.clicked.connect(self.instruction)

    def check_and_save(self):
        try:
            if not YaDisk(token=self.token_input.text().strip('\n')).check_token():
                WrongTokenDialog().exec()
                return
        except UnicodeEncodeError:
            WrongTokenDialog().exec()

        last_session = get_last_session()
        if last_session is None:
            return

        user: AppUser = last_session.user
        config: AppUserConfig = user.config
        config.yandex_api_key = self.token_input.text().strip('\n')
        config.has_valid_token = True
        AppUserConfig.save(config)

        self.close()

    def instruction(self):
        AddLater().exec()

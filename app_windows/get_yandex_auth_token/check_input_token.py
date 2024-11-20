import pyperclip
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from yadisk import YaDisk

from app_windows.dialog_samples import EmptyDialog
from config import TEMPLATES_PATH
from database.models import AppUser, AppUserConfig
from util import get_last_session


class WrongTokenDialog(EmptyDialog):
    INFO = "Указан неверный токен!"


class AskToken(QDialog):
    def __init__(self, link: str):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}ask_token.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.link: str = link

        self.buttonBox.accepted.connect(self.check_token)
        self.buttonBox.rejected.connect(self.close)
        self.submit.clicked.connect(self.check_token)
        self.copy_link.clicked.connect(self.copy_link_to_clipboard)

    def copy_link_to_clipboard(self):
        pyperclip.copy(self.link)

    def check_token(self):
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

    def closeEvent(self, _):
        last_session = get_last_session()
        if last_session is None:
            return False

        return last_session.user.config.has_valid_token

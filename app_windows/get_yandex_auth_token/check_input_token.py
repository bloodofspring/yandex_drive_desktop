import pyperclip
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from yadisk import YaDisk

from app_windows.dialog_samples import EmptyDialog
from app_windows.get_yandex_auth_token.auth_failed import AuthFailed
from config import TEMPLATES_PATH
from database.models import Session, AppUser, AppUserConfig


class WrongTokenDialog(EmptyDialog):
    INFO = "Указан неверный токен!"


class AskToken(QDialog):
    def __init__(self, link: str):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}ask_token.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.link: str = link

        self.buttonBox.accepted.connect(self.check_token)
        self.buttonBox.rejected.connect(lambda self: self.close())
        self.submit.clicked.connect(self.check_token)
        self.copy_link.clicked.connect(self.copy_link_to_clipboard)

    def copy_link_to_clipboard(self):
        pyperclip.copy(self.link)

    def check_token(self):
        if not YaDisk(token=self.token_input.text().strip('\n')).check_token():
            ex_ = WrongTokenDialog()
            ex_.exec()
            return

        try:
            user: AppUser = Session.select().order_by(Session.created_at.desc())[-1].user
        except IndexError:
            AuthFailed().exec()
            return

        config: AppUserConfig = user.config
        config.yandex_api_key = self.token_input.text().strip('\n')
        AppUserConfig.save(config)
        print("token saved!")

        self.close()

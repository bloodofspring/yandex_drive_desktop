import pyperclip
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from app_windows.get_yandex_auth_token.check_input_token import AskToken
from config import TEMPLATES_PATH
from database.models import AppUserConfig
from util import get_last_session


class GetAuthTokenDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}oauth_yandex_dialog.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.check_button_signals()

    def check_button_signals(self):
        self.copy_link.clicked.connect(self.copy_link_to_clipboard)
        self.submit.clicked.connect(self.token_submit_window)
        self.app_creation_instruction.clicked.connect(self.show_app_creation_instruction_dialog)

    @staticmethod
    def show_app_creation_instruction_dialog():
        pass  # nothing here

    @staticmethod
    def copy_link_to_clipboard():
        pyperclip.copy("https://oauth.yandex.ru/client/new/id")

    def token_submit_window(self):
        ex_ = AskToken(f"https://oauth.yandex.ru/authorize?response_type=token&client_id={self.client_id_field.text()}")
        if ex_.exec():
            self.close()

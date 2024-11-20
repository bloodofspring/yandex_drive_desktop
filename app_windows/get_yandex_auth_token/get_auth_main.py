import pyperclip
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from app_windows.get_yandex_auth_token.check_input_token import AskToken
from app_windows.registration.registration_main import RegistrationDialog
from config import TEMPLATES_PATH
from util import get_last_session


class GetAuthTokenDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}oauth_yandex_dialog.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        # last_session = get_last_session()
        # if last_session is not None and last_session.user.config.has_valid_token:
        #     print("closing...")
        #     self.close()
        self.show_registration_dialog()
        self.check_button_signals()

    @staticmethod
    def show_registration_dialog():
        ex_ = RegistrationDialog()
        ex_.exec()

    @staticmethod
    def show_app_creation_instruction_dialog():
        print(1)

    def check_button_signals(self):
        self.copy_link.clicked.connect(self.copy_link_to_clipboard)
        self.submit.clicked.connect(self.token_submit_window)
        self.app_creation_instruction.clicked.connect(self.show_app_creation_instruction_dialog)

    @staticmethod
    def copy_link_to_clipboard():
        pyperclip.copy("https://oauth.yandex.ru/client/new/id")

    def token_submit_window(self):
        ex_ = AskToken(f"https://oauth.yandex.ru/authorize?response_type=token&client_id={self.client_id_field.text()}")
        ex_.exec()

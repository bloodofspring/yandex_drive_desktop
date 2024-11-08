from yadisk import YaDisk
import pyperclip

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog


class WrongTokenDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('wrong_token_dialog.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.buttonBox.accepted.connect(self.check_and_close)
        self.buttonBox.rejected.connect(self.check_and_close)

    def check_and_close(self):
        self.close()


class AskToken(QDialog):
    def __init__(self, link: str):
        super().__init__()
        uic.loadUi('ask_token.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.link: str = link

        self.buttonBox.accepted.connect(self.check_token)
        self.buttonBox.rejected.connect(self.check_and_close)
        self.submit.clicked.connect(self.check_token)
        self.copy_link.clicked.connect(self.copy_link_to_clipboard)

    def copy_link_to_clipboard(self):
        pyperclip.copy(self.link)

    def check_token(self):
        if not YaDisk(token=self.token_input.text().strip('\n')).check_token():
            ex_ = WrongTokenDialog()
            ex_.exec()
            return

        print(f"success! token={self.token_input}")
        # Сохранение токена, переход дальше

    def check_and_close(self):
        self.close()

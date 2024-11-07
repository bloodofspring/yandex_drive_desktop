from PyQt6 import uic
from PyQt6.QtWidgets import QDialog


class WrongTokenDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('.ui', self)
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

        self.buttonBox.accepted.connect(self.check_and_close)
        self.buttonBox.rejected.connect(self.check_and_close)

    def check_and_close(self):
        self.close()

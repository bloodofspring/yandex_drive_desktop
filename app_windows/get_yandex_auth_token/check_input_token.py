from PyQt6 import uic
from PyQt6.QtWidgets import QDialog


class CheckInputToken(QDialog):
    def __init__(self, link_to_get_tkkn: str):
        super().__init__()
        uic.loadUi('.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.buttonBox.accepted.connect(self.check_and_close)
        self.buttonBox.rejected.connect(self.check_and_close)

    def check_and_close(self):
        self.close()

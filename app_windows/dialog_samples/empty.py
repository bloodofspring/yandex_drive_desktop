from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from config import TEMPLATES_PATH


class EmptyDialog(QDialog):
    INFO: str = ""

    def __init__(self):
        super().__init__()
        uic.loadUi(f"{TEMPLATES_PATH}empty_dialog.ui", self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.info.setText(self.INFO)
        self.check_buttons_pushed()

    def check_buttons_pushed(self):
        self.buttonBox.accepted.connect(self.check_and_close)
        self.buttonBox.rejected.connect(self.check_and_close)

    def check_and_close(self):
        self.close()

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from config import TEMPLATES_PATH


class GetAuthTokenDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}change_loginpas_form.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.check_button_signals()

    def check_button_signals(self):
        pass

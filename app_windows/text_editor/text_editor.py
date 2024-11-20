from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from config import TEMPLATES_PATH


class TextEditor(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}img_view_template.ui', self)
        self.setWindowTitle("Text Editor")
        self.setFixedSize(self.size())

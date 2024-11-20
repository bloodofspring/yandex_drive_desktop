from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QTextBrowser

from config import TEMPLATES_PATH


class TextEditor(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}text_editor.ui', self)
        self.setWindowTitle("Text Editor")
        self.setFixedSize(self.size())

    def handle_buttons(self):
        self.save_and_exit.clocked.connect(self.save_and_exit)
        self.dont_save_and_exit.clocked.connect(self.close)
        self.clear_input_field.clocked.connect(self.clear_field)

    def clear_field(self):
        self.input_field.clear()

    def save_and_exit(self):
        self.save_text()
        self.close()

    def load_and_show_text(self):
        pass

    def save_text(self):
        pass

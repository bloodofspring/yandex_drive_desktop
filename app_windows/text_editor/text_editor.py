from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from config import TEMPLATES_PATH
from database.yadisk import YaDiskDownloader
from util import get_last_session


class TextEditor(QDialog):
    def __init__(self, full_file_way: str):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}text_editor.ui', self)
        self.setWindowTitle("Text Editor")
        self.setFixedSize(self.size())
        self.input_field.setReadOnly(False)

        self.file_way = full_file_way
        self.downloaded_file_way: str = ""

        self.load_and_display_text()
        self.handle_buttons()

    def handle_buttons(self):
        self.save_and_exit.clicked.connect(self.save_and_exit_func)
        self.dont_save_and_exit.clicked.connect(self.close)
        self.clear_input_field.clicked.connect(self.clear_field)

    def clear_field(self):
        self.input_field.clear()

    def save_and_exit_func(self):
        self.save_text()
        self.close()

    def load_and_display_text(self):
        session = get_last_session()
        if session is None:
            self.close()

        downloader = YaDiskDownloader(session=session)
        self.downloaded_file_way = downloader.download_file(way=self.file_way)

        with open(self.downloaded_file_way, "r") as f:
            self.input_field.setText(f.read())

    def save_text(self):
        session = get_last_session()
        if session is None:
            self.close()

        with open(self.downloaded_file_way, "w") as f:
            f.write(self.input_field.toPlainText())

        downloader = YaDiskDownloader(session=session)
        downloader.update_file(self.file_way, self.downloaded_file_way)

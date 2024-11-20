import os

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog

from config import TEMPLATES_PATH
from database.yadisk import YaDiskDownloader
from util import get_last_session


class ImageViewer(QDialog):
    def __init__(self, full_file_way: str):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}img_view_template.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна
        self.setWindowTitle("Image Viewer")

        self.file_way = full_file_way

        self.handle_buttons()

    def handle_buttons(self):
        self.back.clicked.connect(self.close)
        self.delete.clicked.connect(self.delete_file_from_yadisk)

    def load_file(self) -> str:
        session = get_last_session()
        if session is None:
            self.close()

        downloader = YaDiskDownloader(session=session)
        return downloader.download_file(way=self.file_way)

    def delete_file_from_yadisk(self):
        print("Not implemented yet")

    def display_file(self):
        name = self.load_file()

        pixmap = QPixmap(name)
        self.image.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height() + 20)

        os.remove(name)

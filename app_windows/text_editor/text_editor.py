import os

from PIL import Image
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QWidget, QGridLayout

from config import TEMPLATES_PATH
from database.yadisk import YaDiskDownloader
from util import get_last_session


class TextEditor(QDialog):
    def __init__(self, full_file_way: str):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}img_view_template.ui', self)
        self.setWindowTitle("Image Viewer")
        self.file_way = full_file_way
        self.display_file()

    def load_file(self) -> str:
        session = get_last_session()
        if session is None:
            self.close()

        downloader = YaDiskDownloader(session=session)
        return downloader.download_file(way=self.file_way)

    def display_file(self):
        name = self.load_file()

        pixmap = QPixmap(name)
        im = Image.open(name)
        width, height = im.size

        if width > 1000:
            width = 1000

        if height > 500:
            height = 500

        self.image.setPixmap(pixmap)
        self.image.resize(width, height)

        layout = QGridLayout()
        layout.addWidget(self.image)
        widget = QWidget()
        widget.setLayout(layout)

        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(widget)
        self.scrollArea.resize(width, height)

        self.setFixedSize(width, height)

        os.remove(name)

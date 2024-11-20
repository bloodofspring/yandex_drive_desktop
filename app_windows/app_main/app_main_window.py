import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QScrollArea, QPushButton, QWidget

from app_windows.app_main.token_error import WrongToken
from config import TEMPLATES_PATH
from database.models import File
from database.yadisk import YaDiskDownloader
from util import get_last_session


class FileMainWindow(QMainWindow):
    def __init__(self, start_path: str = "disk:/"):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}file_main_window.ui', self)
        self.setFixedSize(self.size())

        self.path = start_path

        self.with_user_yadisk()
        self.handle_toolbar()

    def display_data_from_yadisk(self):
        last_session = get_last_session()
        if last_session is None:
            return

        data = YaDiskDownloader(session=last_session).get_path_data(self.path)
        self.display(data=list(map(
            lambda d: {"text": d.name, "callback": "show_file" if isinstance(d, File) else "show_directory"},
            data
        )))

    def show_file(self):
        print(self.sender().text())

    def show_directory(self):
        self.path = self.path + "/" + self.sender().text()
        self.display_data_from_yadisk()

    def display(self, data: list[dict[str, str]], row_width: int = 10, size: int = 100):  # {"text", "callback"}
        x_pos = 0
        y_pos = 0
        layout = QGridLayout()
        scroll = QScrollArea()

        for el in data:
            if len({"text", "callback"} & set(el.keys())) < 2:
                continue  # invalid keys

            if not hasattr(self, el["callback"]):
                continue

            pb = QPushButton()
            pb.setText(el["text"])
            pb.setFixedSize(size, size)
            pb.clicked.connect(getattr(self, el["callback"]))
            layout.addWidget(pb, y_pos, x_pos)

            x_pos += 1

            if x_pos > row_width:
                x_pos = 0
                y_pos += 1

        widget = QWidget()
        widget.setLayout(layout)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        self.setFixedWidth(layout.maximumSize().width())
        self.setCentralWidget(scroll)

    @staticmethod
    def with_user_yadisk():
        last_session = get_last_session()
        if last_session is None:
            return

        downloader = YaDiskDownloader(session=last_session)
        if not downloader.load_user_yadisk():
            WrongToken().exec()

    def handle_toolbar(self):
        self.action_3.triggered.connect(self.debug_action)
        self.action_4.triggered.connect(self.debug_action)
        self.action_5.triggered.connect(self.debug_action)
        self.action_6.triggered.connect(self.debug_action)
        self.action_7.triggered.connect(self.debug_action)
        self.action_8.triggered.connect(self.debug_action)
        self.action_9.triggered.connect(self.debug_action)
        self.action_10.triggered.connect(self.debug_action)

    def debug_action(self, s):
        print("click", s, self.sender().text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileMainWindow()
    ex.show()
    sys.exit(app.exec())

import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QScrollArea, QPushButton, QWidget

from app_windows.get_yandex_auth_token import GetAuthTokenDialog
from app_windows.app_main.not_implemented_yet import AddLater
from app_windows.app_main.updating_dialog import Updating
from app_windows.change_loginpas_form import ChangeLoginpasDialog
from app_windows.change_token_form import ChangeAuthTokenDialog
from app_windows.img_viewer import ImageViewer
from app_windows.registration import RegistrationDialog
from app_windows.text_editor import TextEditor
from config import TEMPLATES_PATH
from database.models import File, Session
from database.yadisk import YaDiskDownloader
from util import get_last_session


class FileMainWindow(QMainWindow):
    def __init__(self, start_path: str = "disk:/"):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}file_main_window.ui', self)
        self.setFixedSize(self.size())

        self.path = self.start_path = start_path
        self.session = get_last_session(show_alert=False)  # Получение сесси

        self.check_reqs()
        self.handle_toolbar()

    def update_session(self):
        latest_session = get_last_session(show_alert=False)
        if latest_session is None:
            return

        self.session = latest_session

    def check_reqs(self):
        if self.session is None:
            RegistrationDialog().exec()  # Создание сессии
            self.session = get_last_session(show_alert=False)
            self.check_reqs()  # Будем доставать пользователей пока не выполнят все нужные условия ))

        if not self.session.user.config.has_valid_token:
            GetAuthTokenDialog().exec()  # Получение валидного токена
            self.update_session()
            self.check_reqs()  # Будем доставать пользователей пока не выполнят все нужные условия ))

        self.update_data()
        self.render_window()

    def update_data(self):
        downloader = YaDiskDownloader(session=self.session)
        Updating().exec()
        downloader.load_user_yadisk()

    def to_prev_path(self):
        self.path = "/".join(self.path.rstrip("/").split("/")[:-1]) + "/"
        self.render_window()

    def show_file(self):
        file_name = self.sender().text()
        full_way = self.path + file_name + "/"

        if file_name.endswith(".txt"):
            TextEditor(full_file_way=full_way).exec()
            return

        if any(map(lambda e: file_name.endswith(e), (".jpg", ".jpeg", ".png"))):
            ImageViewer(full_file_way=full_way).exec()
            return

    def show_directory(self):
        self.path = self.path + self.sender().text() + "/"
        self.render_window()

    def render_window(self):
        downloader = YaDiskDownloader(session=self.session)
        data = downloader.get_path_data(self.path)

        to_display = list(map(
            lambda d: {"text": d.name, "callback": "show_file" if isinstance(d, File) else "show_directory"},
            data
        ))

        if not to_display:
            to_display = [{"text": "nothing here", "callback": "to_prev_path"}]

        if self.path != self.start_path:
            to_display = [{"text": "return", "callback": "to_prev_path"}] + to_display

        self.display(data=to_display)

    def display(self, data: list[dict[str, str]], row_width: int = 5, size: int = 200):  # {"text", "callback"}
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

    def handle_toolbar(self):
        self.action_3.triggered.connect(lambda _: AddLater().exec())
        self.action_4.triggered.connect(lambda _: ChangeAuthTokenDialog().exec())
        self.action_5.triggered.connect(lambda _: AddLater().exec())
        self.action_6.triggered.connect(lambda _: AddLater().exec())
        self.action_7.triggered.connect(lambda _: ChangeLoginpasDialog().exec())
        self.action_8.triggered.connect(lambda _: AddLater().exec())
        self.action_9.triggered.connect(lambda _: AddLater().exec())
        self.action_10.triggered.connect(self.update_data)

    def closeEvent(self, _):
        Session.truncate_table()  # ha-ha-ha.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileMainWindow()
    ex.show()
    sys.exit(app.exec())

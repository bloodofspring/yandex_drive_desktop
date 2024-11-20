# ToDo: Удалить логи
# ToDo: Выровнять код
import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QScrollArea, QPushButton, QWidget

from app_windows import GetAuthTokenDialog
from app_windows.registration import RegistrationDialog
from config import TEMPLATES_PATH
from database.models import File, FileDirectory, Session
from database.yadisk import YaDiskDownloader
from util import get_last_session


class FileMainWindow(QMainWindow):
    def __init__(self, start_path: str = "disk:/"):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}file_main_window.ui', self)
        self.setFixedSize(self.size())

        self.path = self.start_path = start_path

        self.check_reqs()
        self.handle_toolbar()

    def check_reqs(self):
        if self.last_session is None:
            RegistrationDialog().exec()  # Создание сессии

        if not self.last_session.user.config.has_valid_token:
            GetAuthTokenDialog().exec()  # Получение валидного токена

        self.check_reqs()  # Будем доставать пользователей пока не выполнят все нужные условия ))

        self.update_data()
        self.render_window()


    @property
    def last_session(self) -> Session | None:
        last_session = get_last_session(show_alert=False)
        if last_session is None:
            return

        return last_session

    @staticmethod
    def update_data():
        last_session = get_last_session(show_alert=False)
        if last_session is None:
            return

        downloader = YaDiskDownloader(session=last_session)
        downloader.load_user_yadisk()

    def to_prev_path(self):
        self.path = "/".join(self.path.rstrip("/").split("/")[:-1]) + "/"
        print(999999999999, self.path)
        self.display_data_from_yadisk()

    def show_file(self):
        print(self.sender().text())

    def show_directory(self):
        self.path = self.path + self.sender().text() + "/"
        # self.path = self.path.strip("/")
        print(1192831290283912, self.path)

        self.display_data_from_yadisk()

    def render_window(self, show_alert: bool = True):
        last_session = get_last_session(show_alert=show_alert)
        if last_session is None:
            return

        downloader = YaDiskDownloader(session=last_session)
        # downloader.load_user_yadisk()
        data = downloader.get_path_data(self.path)
        print(*map(lambda x: x.full_way, FileDirectory.select()), sep=" || ")
        print(self.path, data)
        to_display = list(map(
            lambda d: {"text": d.name, "callback": "show_file" if isinstance(d, File) else "show_directory"},
            data
        ))

        if not to_display:
            to_display = [{"text": "nothing here", "callback": "to_prev_path"}]

        if self.path != self.start_path:
            to_display = [{"text": "return", "callback": "to_prev_path"}] + to_display

        self.display(data=to_display)

    def display(self, data: list[dict[str, str]], row_width: int = 10, size: int = 200):  # {"text", "callback"}
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

    @property
    def need_valid_token(self):
        last_session = get_last_session()
        return (last_session is None) or (not last_session.user.config.has_valid_token)

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

    def closeEvent(self, _):
        Session.truncate_table()  # ha-ha-ha.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileMainWindow()
    ex.show()
    sys.exit(app.exec())

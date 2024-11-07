import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication

from app_windows.get_yandex_auth_token.check_input_token import CheckInputToken
from database import create_tables


class RegistrationMain(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('oauth_yandex_template_main.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.check_button_signals()

    def check_button_signals(self):
        self.submit.clicked.connect(self.token_submit_window)

    @staticmethod
    def token_submit_window():
        ex_ = CheckInputToken(link_to_get_tkkn=f"")
        ex_.exec()


# Для тестов
if __name__ == '__main__':
    create_tables()
    app = QApplication(sys.argv)
    ex = RegistrationMain()
    ex.show()
    sys.exit(app.exec())


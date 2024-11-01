import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication

from database import create_tables


class RegistrationMain(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('oauth_yandex_main_template.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.check_button_signals()

    def check_button_signals(self):
        self.submit.clicked.connect(self.token_submit_window)

    @staticmethod
    def token_submit_window():
        ex_ = ...()
        ex_.exec()


# Для тестов
if __name__ == '__main__':
    create_tables()
    app = QApplication(sys.argv)
    ex = RegistrationMain()
    ex.show()
    sys.exit(app.exec())


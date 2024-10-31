import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication


class RegistrationMain(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('reg_page_template.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.check_button_signals()

    def check_button_signals(self):
        self.enter_button.clicked.connect(self.check_user_data)
        self.reg_button.clicked.connect(self.registrate_new_user)

    def check_user_data(self):
        pass

    def registrate_new_user(self):
        pass


# Для тестов
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegistrationMain()
    ex.show()
    sys.exit(app.exec())

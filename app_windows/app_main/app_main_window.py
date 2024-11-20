import sys

from PyQt6 import uic
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication

from config import TEMPLATES_PATH


class FileMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{TEMPLATES_PATH}file_main_window.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.handle_toolbar()

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

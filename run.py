import sys

from PyQt6.QtWidgets import QApplication

from app_windows import GetAuthTokenDialog
from database import create_tables


class AppRunner:
    def __init__(self):
        pass

    @staticmethod
    def run():
        create_tables()
        app = QApplication(sys.argv)
        ex = GetAuthTokenDialog()
        ex.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    app_runner = AppRunner()
    app_runner.run()

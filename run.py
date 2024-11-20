import sys

from PyQt6.QtWidgets import QApplication

from app_windows import GetAuthTokenDialog
from app_windows.app_main import FileMainWindow
from app_windows.registration import RegistrationDialog
from database import create_tables


class AppRunner:
    def __init__(self):
        pass

    @staticmethod
    def registration():
        RegistrationDialog().exec()

    @staticmethod
    def get_token():
        GetAuthTokenDialog().exec()

    def check_main_window_state(self, window_instance: FileMainWindow):
        if window_instance.need_registration:
            self.registration()
            window_instance.update_()

        if window_instance.need_valid_token:
            self.get_token()
            window_instance.update_()

    def run(self):
        create_tables()
        app = QApplication(sys.argv)
        ex = FileMainWindow()
        # self.check_main_window_state(window_instance=ex)
        ex.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    app_runner = AppRunner()
    app_runner.run()

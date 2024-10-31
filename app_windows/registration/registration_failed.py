from PyQt6 import uic
from PyQt6.QtWidgets import QDialog


class RegistrationFailed(QDialog):
    def __init__(self, error_message: str):
        super().__init__()
        uic.loadUi('registration_failed_template.ui', self)
        self.setFixedSize(self.size())  # Запретить изменение окна

        self.error_label.setText(error_message)

        self.buttonBox.accepted.connect(self.__close)
        self.buttonBox.rejected.connect(self.__close)

    def __close(self):
        self.close()

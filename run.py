import sys

from PyQt6.QtWidgets import QApplication

from app_windows import FileMainWindow
from database import create_tables

if __name__ == "__main__":
    create_tables()
    app = QApplication(sys.argv)
    ex = FileMainWindow()
    ex.show()
    sys.exit(app.exec())

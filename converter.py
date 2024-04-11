import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from multiool_app import MultiToolApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MultiToolApp()
    main_window.show()
    sys.exit(app.exec_())

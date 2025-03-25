from PyQt5.QtWidgets import QFormLayout
from mutagen.easyid3 import EasyID3
import sys
import os
from time import sleep
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import configparser
from mutagen import File


class MetadataEditor(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.formats = config.get('audio', 'mutagen_formats').split(',')
        self.formats = [format.lower() for format in self.formats]

        self.layout = QVBoxLayout(self)

        self.folder_button = QPushButton("")
        self.folder_button.clicked.connect(self.choose_directory)
        self.layout.addWidget(self.folder_button)

        self.folder_label = QLabel()
        self.layout.addWidget(self.folder_label)

        self.artist_label = QLabel("")
        self.layout.addWidget(self.artist_label)
        self.artist_input = QLineEdit(self)
        self.layout.addWidget(self.artist_input)

        self.album_label = QLabel("")
        self.layout.addWidget(self.album_label)
        self.album_input = QLineEdit(self)
        self.layout.addWidget(self.album_input)

        self.date_label = QLabel("")
        self.layout.addWidget(self.date_label)
        self.date_input = QLineEdit(self)
        self.layout.addWidget(self.date_input)

        self.genre_label = QLabel("")
        self.layout.addWidget(self.genre_label)
        self.genre_input = QLineEdit(self)
        self.layout.addWidget(self.genre_input)

        self.year_label = QLabel("")
        self.layout.addWidget(self.year_label)
        self.year_input = QLineEdit(self)
        self.layout.addWidget(self.year_input)

        self.progress_label = QLabel(self)
        self.layout.addWidget(self.progress_label)

        self.apply_button = QPushButton("")
        self.apply_button.clicked.connect(self.apply_metadata)
        self.layout.addWidget(self.apply_button)

    def load_language(self, lang_dict):
        self.folder_button.setText(lang_dict["choose_directory"])
        self.choose_directory_text = lang_dict["choose_directory"]
        self.apply_button.setText(lang_dict["apply"])
        self.artist_label.setText(lang_dict["artist"])
        self.album_label.setText(lang_dict["album"])
        self.date_label.setText(lang_dict["date"])
        self.genre_label.setText(lang_dict["genre"])
        self.year_label.setText(lang_dict["year"])
        self.warning_text = lang_dict["warning"]
        self.modified_metadata_text = lang_dict["modified_metadata"]
        self.unsupported_text = lang_dict["unsupported"]

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, self.choose_directory_text)
        if directory:
            self.folder_label.setText(directory)

    def apply_metadata(self):
        if self.folder_label.text() == "":
            QMessageBox.warning(self, self.warning_text,
                                self.choose_directory_text)
            return
        else:
            directory = self.folder_label.text()
            files = os.listdir(directory)
            files = [file for file in files if file.lower().endswith(
                tuple(self.formats))]
            for file in files:
                filepath = os.path.join(directory, file)
                self.modify_metadata(filepath)

        self.progress_label.setText(self.modified_metadata_text)
        QApplication.processEvents()
        sleep(2)
        self.progress_label.setText("")
        QApplication.processEvents()

    def modify_metadata(self, file_path):
        try:
            audio = File(file_path)

            if audio is None:
                print(f"{self.unsupported_text} : {file_path}")
                return

            if not audio.tags:
                audio.add_tags()

            audio.update({
                'artist': self.artist_input.text(),
                'album': self.album_input.text(),
                'genre': self.genre_input.text(),
                'date': self.date_input.text(),
                'year': self.year_input.text()
            })
            audio.save()
        except Exception as e:
            QMessageBox.critical(self, self.error, str(e))

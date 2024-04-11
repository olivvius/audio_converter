from PyQt5.QtWidgets import QFormLayout
from mutagen.easyid3 import EasyID3
import sys, os
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

        self.artist_label = QLabel("Artist:")
        self.layout.addWidget(self.artist_label)
        self.artist_input = QLineEdit(self)
        self.layout.addWidget(self.artist_input)

        self.album_label = QLabel("album:")
        self.layout.addWidget(self.album_label)
        self.album_input = QLineEdit(self)
        self.layout.addWidget(self.album_input)
        
        self.date_label = QLabel("date:")
        self.layout.addWidget(self.date_label)
        self.date_input = QLineEdit(self)
        self.layout.addWidget(self.date_input)
        
        self.genre_label = QLabel("genre:")
        self.layout.addWidget(self.genre_label)
        self.genre_input = QLineEdit(self)
        self.layout.addWidget(self.genre_input)

        self.progress_label = QLabel(self)
        self.layout.addWidget(self.progress_label)

        self.apply_button = QPushButton("Appliquer")
        self.apply_button.clicked.connect(self.apply_metadata)
        self.layout.addWidget(self.apply_button)

    def load_language(self, lang_dict):
        self.folder_button.setText(lang_dict["choose_directory"])
        self.choose_directory_text = lang_dict["choose_directory"]
        self.artist_text = lang_dict["artist"]

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, self.choose_directory_text)
        if directory:
            self.folder_label.setText(directory)

    def apply_metadata(self):
        if self.folder_label.text() == "":
            QMessageBox.warning(self, "Warning", "Please choose a directory")
            return
        else:
            directory = self.folder_label.text()
            files = os.listdir(directory)
            files = [file for file in files if file.lower().endswith(tuple(self.formats))]
            for file in files:
                    filepath = os.path.join(directory, file)
                    self.modify_metadata(filepath)

        self.progress_label.setText("chgt metadata applied")
        QApplication.processEvents()
        sleep(2)
        self.progress_label.setText("")
        QApplication.processEvents()

            
    def modify_metadata(self, file_path):
        try:
            audio = File(file_path)

            if audio is None:
                print(f"Format non pris en charge pour le fichier : {file_path}")
                return
            
            if audio.tags:
                del audio['artist']
                del audio['album']
                del audio['genre']
                del audio['date']

            if not audio.tags:
                audio.add_tags()

            audio['artist'] = self.artist_input.text()
            audio['album'] = self.album_input.text()
            audio['genre'] = self.genre_input.text()
            audio['date'] = self.date_input.text()
            audio.save()
            print(f"Métadonnées modifiées pour le fichier : {file_path}")

        except Exception as e:
            print(f"Une erreur s'est produite lors de la modification des métadonnées pour le fichier {file_path} : {str(e)}")


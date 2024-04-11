import sys, os
from time import sleep
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import configparser
import soundfile as sf

class MassAudioConverter(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)

        self.folder_button = QPushButton("")
        self.folder_button.clicked.connect(self.choose_directory)
        self.layout.addWidget(self.folder_button)

        self.folder_label = QLabel()
        self.layout.addWidget(self.folder_label) 

        self.format_label = QLabel("Format de sortie:")
        self.layout.addWidget(self.format_label)

        config = configparser.ConfigParser()
        config.read('settings.ini')

        self.formats = config.get('audio', 'formats').split(',')
        self.formats_list = ' '.join(f'*.{format}' for format in self.formats)
        self.format_combo = QComboBox()
        self.format_combo.addItems(self.formats)
        self.layout.addWidget(self.format_combo)

        self.samplerate_label = QLabel("samplerate de sortie:")
        self.layout.addWidget(self.samplerate_label)
        self.samplerate_combo = QComboBox()
        self.samplerates = config['audio']['samplerates'].split(',')
        self.samplerate_combo.addItems(self.samplerates)
        self.layout.addWidget(self.samplerate_combo)

        self.suffix_label = QLabel("Suffixe de sortie:")
        self.layout.addWidget(self.suffix_label)
        self.suffix_input = QLineEdit(self)
        self.layout.addWidget(self.suffix_input)

        self.convert_button = QPushButton("Conversion")
        self.convert_button.clicked.connect(self.convert_file)
        self.layout.addWidget(self.convert_button)

        self.progress_label = QLabel(self)
        self.layout.addWidget(self.progress_label)

    def load_language(self, lang_dict):
        self.folder_button.setText(lang_dict["choose_directory"])
        self.choose_directory_text = lang_dict["choose_directory"]
        self.format_label.setText(lang_dict["output_format"])
        self.samplerate_label.setText(lang_dict["output_samplerate"])
        self.convert_button.setText(lang_dict["convert"])
        self.choose_file_text = lang_dict["choose_file"]
        self.converted_text = lang_dict["converted"]
        self.audio_files = lang_dict["audio_files"]
        self.conversion = lang_dict["conversion"]
        self.suffix_label.setText(lang_dict["output_suffix"])
        self.converting_file_text = lang_dict["converting_file"]
        self.complete_conversion_text = lang_dict["complete_conversion"]
        self.error_text = lang_dict["error"]


    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, self.choose_directory_text)
        if directory:
            self.folder_label.setText(directory)

    def convert_file(self):
        if self.folder_label.text() == "":
            QMessageBox.warning(self, "Warning", "Please choose a directory")
            return

        selected_format = self.format_combo.currentText().lower()
        selected_samplerate = int(self.samplerate_combo.currentText())
        source_directory = self.folder_label.text()
        suffix = self.suffix_input.text()

        files = os.listdir(source_directory)
        total_files = len(files)
        converted_files = 0

        for file in files:
            source_file = os.path.join(source_directory, file)
            converted_files += 1
            self.progress_label.setText(f" {self.converting_file_text} {converted_files} / {total_files}")
            QApplication.processEvents()
            try:
                data, samplerate = sf.read(source_file)
                output_file = source_file.rsplit('.', 1)[0] + suffix + '.' + selected_format
                
                if selected_format == 'raw':
                    subtype = 'PCM_16'
                    sf.write(output_file, data, selected_samplerate, subtype=subtype)
                else:
                    sf.write(output_file, data, selected_samplerate, format=selected_format)
                


            except Exception as e:
                print(f"{self.error_text} {file}: {e}")
                continue
        
        self.progress_label.setText(self.complete_conversion_text)
        QApplication.processEvents()
        sleep(2)
        self.progress_label.setText("")
        QApplication.processEvents()


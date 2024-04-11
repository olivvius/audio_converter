import sys
from time import sleep
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import configparser
import soundfile as sf
import numpy as np
from scipy import signal

class SingleAudioConverter(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)
        
        self.file_button = QPushButton("Choisir fichier")
        self.file_button.clicked.connect(self.choose_file)
        self.layout.addWidget(self.file_button)

        self.file_label = QLabel()
        self.layout.addWidget(self.file_label) 

        self.format_label = QLabel("Format de sortie:")
        self.layout.addWidget(self.format_label)

        config = configparser.ConfigParser()
        config.read('settings.ini')

        self.formats = config.get('audio', 'formats').split(',')
        self.formats_list = ' '.join(f'*.{format}' for format in self.formats)
        self.format_combo = QComboBox()
        
        self.format_combo.addItems(self.formats)
        self.layout.addWidget(self.format_combo)

        self.samplerate_label = QLabel("Sample rate de sortie:")
        self.layout.addWidget(self.samplerate_label)
        self.samplerate_combo = QComboBox()
        self.samplerates = config['audio']['samplerates'].split(',')
        self.samplerate_combo.addItems(self.samplerates)
        self.layout.addWidget(self.samplerate_combo)

        self.suffix_label = QLabel("Suffixe de sortie:")
        self.layout.addWidget(self.suffix_label)
        self.suffix_input = QLineEdit(self)
        self.layout.addWidget(self.suffix_input)

        self.begin_input = None
        self.end_input = None

        hbox = QHBoxLayout()
        self.begin_label = QLabel("debut (sec):")
        self.begin_input = QLineEdit(self)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.begin_label)
        vbox1.addWidget(self.begin_input)
        self.end_label = QLabel("fin (sec):")
        self.end_input = QLineEdit(self)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.end_label)
        vbox2.addWidget(self.end_input)
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        self.layout.addLayout(hbox)

        self.convert_button = QPushButton("Conversion")
        self.convert_button.clicked.connect(self.convert_file)
        self.layout.addWidget(self.convert_button)

        self.progress_label = QLabel(self)
        self.layout.addWidget(self.progress_label)

    def load_language(self, lang_dict):
        self.file_button.setText(lang_dict["choose_file"])
        self.format_label.setText(lang_dict["output_format"])
        self.samplerate_label.setText(lang_dict["output_samplerate"])
        self.convert_button.setText(lang_dict["convert"])
        self.choose_file_text = lang_dict["choose_file"]
        self.converted_text = lang_dict["converted"]
        self.audio_files = lang_dict["audio_files"]
        self.conversion = lang_dict["conversion"]
        self.suffix_label.setText(lang_dict["output_suffix"])
        self.begin_label.setText(lang_dict["begin"])
        self.end_label.setText(lang_dict["end"])
        self.error_text = lang_dict["error"]
        self.file_error_text = lang_dict["file_error"]
        self.integer_value_error = lang_dict["integer_value_error"]
        self.begin_error = lang_dict["begin_error"]
        self.positive_error = lang_dict["positive_error"]
        self.converting_text = lang_dict["converting"]
        self.complete_conversion_text = lang_dict["complete_conversion"]
        

    def choose_file(self):

        filename, _ = QFileDialog.getOpenFileName(self, self.choose_file_text, "", f"{self.audio_files} ({self.formats_list})")
        if filename:
            self.file_label.setText(filename)
        
    def convert_file(self):

        if self.file_label.text() == "":
            QMessageBox.critical(self, self.error_text, self.file_error_text)
            return
        try:
            begin = int(self.begin_input.text())
            end = int(self.end_input.text())
        except Exception as e:
            QMessageBox.critical(self, self.error_text, self.integer_value_error)
            return
        if begin > end:
            QMessageBox.critical(self, self.error_text, self.begin_error)
            return
        if begin < 0 or end < 0:
            QMessageBox.critical(self, self.error_text, self.positive_error)
            return
        
        self.progress_label.setText(self.converting_text)
        QApplication.processEvents()

        selected_format = self.format_combo.currentText().lower()
        selected_samplerate = int(self.samplerate_combo.currentText())
        source_file = self.file_label.text()
        suffix = self.suffix_input.text()
        
        output_file = source_file.rsplit('.', 1)[0] + suffix + '.' + selected_format
        data, samplerate = sf.read(source_file)
        resampled_data = signal.resample(data, int(len(data) * selected_samplerate / samplerate))
        data = resampled_data

        samplerate = selected_samplerate
        
        try: 
            if self.begin_input.text() == "" and self.end_input.text() == "" :
                if selected_format == 'raw':
                    subtype = 'PCM_16'
                    sf.write(output_file, data, samplerate, subtype=subtype)
                else:
                    sf.write(output_file, data, samplerate, format=selected_format)
            else:
                try:
                    begin = int(self.begin_input.text()) if self.begin_input.text().strip() else 0
                    end = int(self.end_input.text()) if self.end_input.text().strip() else len(resampled_data)
                except Exception as e:
                    QMessageBox.critical(self, self.error_text, str(e))
                
                data = data[int(begin * samplerate):int(end * samplerate)]

                if selected_format == 'raw':
                    subtype = 'PCM_16'
                    sf.write(output_file, data, samplerate, subtype=subtype)
                else:
                    sf.write(output_file, data, samplerate, format=selected_format)

            QMessageBox.information(self, self.conversion, f"{self.converted_text} {output_file}")
        except Exception as e:
            QMessageBox.critical(self, self.error_text, str(e))

        self.progress_label.setText(self.complete_conversion_text)
        QApplication.processEvents()
        sleep(2)
        self.progress_label.setText("")
        QApplication.processEvents()

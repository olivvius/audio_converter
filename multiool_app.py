import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import configparser
from converter_audio import SingleAudioConverter
from mass_converter_audio import MassAudioConverter
from menu import Menu
import json
from LanguageLoader import LanguageLoader
from MetadataEditor import MetadataEditor

class MultiToolApp(QMainWindow):
    def __init__(self):
        super().__init__()

        config = configparser.ConfigParser()
        config.read('settings.ini')

        self.setWindowIcon(QIcon('audio_converter.ico'))
        self.language_loader = LanguageLoader(self)
        self.menu = Menu(self)

        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        width = int( screen_size.width() * float(config['WindowSize']['width']))
        height = int(screen_size.height() * float(config['WindowSize']['height']))
        self.resize(width, height)

        with open('dict/english.json', 'r') as f:
            self.lang = json.load(f)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        self.single_audio_tab = SingleAudioConverter(self)
        self.mass_audio_tab = MassAudioConverter(self)
        self.metadata_tab = MetadataEditor(self)

        self.tabs.addTab(self.single_audio_tab, "")
        self.tabs.addTab(self.mass_audio_tab, "")
        self.tabs.addTab(self.metadata_tab, "")

        self.language_loader.load_language('english')     
        
        if 'Appearance' in config:
            appearance_settings = config['Appearance']
            font = appearance_settings.get('font', 'Arial')
            font_size = appearance_settings.getint('font_size', 12)
            font_color = appearance_settings.get('font_color', '#000000')
            self.setStyleSheet(f"font-family: {font}; font-size: {font_size}px; color: {font_color};")
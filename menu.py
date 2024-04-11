from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication
import sys
import json

class Menu:
    def __init__(self, window):
        self.window = window
        self.initUI()

    def initUI(self):
        menubar = self.window.menuBar()

        self.fileMenu = menubar.addMenu('File')
        self.settingsMenu = menubar.addMenu('Settings')
        self.helpMenu = menubar.addMenu('Help')

        self.exitAct = QAction('Exit', self.window)
        self.exitAct.triggered.connect(self.window.close)
        self.fileMenu.addAction(self.exitAct)

        self.settingsAct = QAction('Preferences', self.window)
        self.settingsMenu.addAction(self.settingsAct)

        self.helpAct = QAction('View Help', self.window)
        self.aboutAct = QAction('About', self.window)
        self.helpMenu.addAction(self.helpAct)
        self.helpMenu.addAction(self.aboutAct)

        self.languageMenu = QMenu('Language', self.window)
        self.englishAct = QAction('English', self.window)
        self.englishAct.triggered.connect(lambda: self.window.language_loader.load_language('english'))
        self.frenchAct = QAction('French', self.window)
        self.frenchAct.triggered.connect(lambda: self.window.language_loader.load_language('french'))
        self.languageMenu.addAction(self.englishAct)
        self.languageMenu.addAction(self.frenchAct)
        menubar.addMenu(self.languageMenu)

    def load_language(self, lang_dict):
        self.fileMenu.setTitle(lang_dict["file"])
        self.settingsMenu.setTitle(lang_dict["settings"])
        self.helpMenu.setTitle(lang_dict["help"])
        self.exitAct.setText(lang_dict["exit"])
        self.settingsAct.setText(lang_dict["preferences"])
        self.helpAct.setText(lang_dict["view_help"])
        self.aboutAct.setText(lang_dict["about"])
        self.languageMenu.setTitle(lang_dict["language"])
        self.englishAct.setText(lang_dict["english"])
        self.frenchAct.setText(lang_dict["french"])
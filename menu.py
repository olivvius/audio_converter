from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication
import sys
import json
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget
import os


class Menu:
    def __init__(self, window):
        self.window = window
        self.settings = QSettings("settings.ini", QSettings.IniFormat)
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
        self.frenchAct = QAction('French', self.window)
        self.spanishAct = QAction('Spanish', self.window)
        self.hindiAct = QAction('Hindi', self.window)
        self.englishAct.triggered.connect(
            lambda: self.window.language_loader.load_language('english'))
        self.frenchAct.triggered.connect(
            lambda: self.window.language_loader.load_language('french'))
        self.spanishAct.triggered.connect(
            lambda: self.window.language_loader.load_language('spanish'))
        self.hindiAct.triggered.connect(
            lambda: self.window.language_loader.load_language('hindi'))
        self.languageMenu.addAction(self.englishAct)
        self.languageMenu.addAction(self.frenchAct)
        self.languageMenu.addAction(self.spanishAct)
        self.languageMenu.addAction(self.hindiAct)
        menubar.addMenu(self.languageMenu)

        self.themeMenu = menubar.addMenu('Theme')
        self.lightThemeAct = QAction('Light', self.window)
        self.lightThemeAct.triggered.connect(lambda: self.load_theme('light'))
        self.darkThemeAct = QAction('Dark', self.window)
        self.darkThemeAct.triggered.connect(lambda: self.load_theme('dark'))
        self.themeMenu.addAction(self.lightThemeAct)
        self.themeMenu.addAction(self.darkThemeAct)

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

    def load_theme(self, theme_name):
        self.settings.beginGroup(theme_name)

        font = self.settings.value('font', 'Arial')
        font_size = int(self.settings.value('font_size', 12))
        font_color = self.settings.value('font_color', '#000000')
        background_color = self.settings.value('background_color', '#FFFFFF')

        self.settings.endGroup()

        style = f"""
            QWidget {{
                background-color: {background_color};
                font-family: {font};
                font-size: {font_size}px;
                color: {font_color};
            }}
            QTabBar::tab {{
                background: {background_color};
                color: {font_color};
            }}
            QTabBar::tab:selected {{
                background: {background_color};
                color: {font_color};
            }}
            QTabWidget::pane {{
                border: 0;
                background: {background_color};
            }}
        """
        self.window.setStyleSheet(style)

        for widget in self.window.findChildren(QWidget):
            QApplication.instance().style().unpolish(widget)
            QApplication.instance().style().polish(widget)
            widget.update()

        self.save_settings(theme_name)

    def save_settings(self, theme_name):
        self.settings.setValue('theme', theme_name)

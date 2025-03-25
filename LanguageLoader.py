import json
from PyQt5.QtCore import QSettings


class LanguageLoader:
    def __init__(self, app):
        self.app = app
        self.lang = {}
        self.settings = QSettings("settings.ini", QSettings.IniFormat)

    def load_language(self, language):
        with open(f'dict/{language}.json', 'r') as f:
            self.lang = json.load(f)

        self.app.setWindowTitle(self.lang["title"])
        self.app.tabs.setTabText(0, self.lang["single_audio_converter"])
        self.app.tabs.setTabText(1, self.lang["mass_audio_converter"])
        self.app.tabs.setTabText(2, self.lang["MetadataEditor"])

        self.app.menu.load_language(self.lang)
        self.app.single_audio_tab.load_language(self.lang)
        self.app.mass_audio_tab.load_language(self.lang)
        self.app.metadata_tab.load_language(self.lang)

        self.save_settings(language)

    def save_settings(self, language):
        self.settings.setValue('language', language)

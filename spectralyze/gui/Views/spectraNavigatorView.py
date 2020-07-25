
from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSizePolicy, QLabel
from PyQt5 import QtCore
from spectralyze.gui.Models.spectraModelWrappers import deimos1DSpectra
from spectralyze.gui.Views.spectraToolboxView import spectraToolboxView
import sys
import os
from time import sleep
import toml

class spectraNavigatorView(QWidget):
    """
    A widget for displaying a spectrum and associate navigator widgets
    """
    CONFIG_FILE = os.path.join(os.environ['SPECTRALYZE_CONFIG'], "spectra_navigator.toml")
    def __init__(self, model, config_type):
        super().__init__()
        self.model = model
        self.modelWidget = model.getWidget()
        self.config_type = config_type
        self.config = toml.load(self.CONFIG_FILE)
        self.setupConfig()
        self.setupWidgets()

    def setupConfig(self):
        self.toolboxView = spectraToolboxView(self.config[self.config_type]['toolbox'])

    def setupWidgets(self):
        """
        For now, a spectraNavigatorView only has two widgets.
        The widget from the spectra model itself
        And a toolbox widget that can interact with that model
        """
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.modelWidget)
        self.layout.addWidget(self.toolboxView)
        self.model.connectToolbox(self.toolboxView)
        self.setLayout(self.layout)

from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal
import Widgets.spectraNavigatorWidgets as widgets
from configparser import ConfigParser
import toml
from importlib import import_module
from copy import copy
from collections import OrderedDict as od
import os

class spectraToolboxView(QWidget):
    CONFIG_FILE = os.path.join(os.environ['SPECTRALYZE_CONFIG'], "toolbox_view.toml")

    """
    UI Element for use with spectra views.
    ------Tools--------
    Next/Prev buttons
    Smoothing widget
    Redshift guess input/display
    """

    signal = pyqtSignal(dict)
    
    def __init__(self, config_type):
        super().__init__()
        print(self.CONFIG_FILE)
        self.config_type = config_type
        self.config = toml.load(self.CONFIG_FILE)
        self.layout = QVBoxLayout()

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(self.verticalSpacer)

        self.setupWidgets()
        self.setLayout(self.layout)
        self.connectSignals()

    
    def setupWidgets(self):
        self.widgets = {}
        mod = None
        for key, val in self.config['general']['widgets'].items():
            if key == 'import':
                mod = import_module(val)
            elif key in self.config[self.config_type]['widgets'].keys():
                class_type = getattr(mod, val)
                widget = class_type(self.config[self.config_type]['widgets'][key])
                self.widgets.update({key: widget})
                self.layout.addWidget(widget)
            else:
                class_type = getattr(mod, val)
                widget = class_type()
                self.widgets.update({key: widget})
                self.layout.addWidget(widget)
    
    def connectSignals(self):
        for name, widget in self.widgets.items():
            if hasattr(widget, "signal"):
                widget.signal.connect(lambda x, y=name: self.signal.emit({y: x}))
    
    def update(self, data):
        for key, value in data.items():
            if key in self.widgets.keys():
                self.widgets[key].update(value)



if __name__ == "__main__":
    app = QApplication([])
    window = spectraToolboxView("keck1d")
    window.show()
    app.exec_()
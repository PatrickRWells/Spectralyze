from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal
from configparser import ConfigParser
import toml
from importlib import import_module
from copy import copy
from collections import OrderedDict as od
import os

class spectraToolboxView(QWidget):

    """
    UI Element for use with data views.
    ------Tools--------
    Which widgets to display are determined by the appropriate config type
    Which should be one of hte configs laid out in the toolbox_view config file
    The signal will emit a dictionary the tool name as key, and a dictionary
    with the data as a value
    """

    signal = pyqtSignal(dict)

    def __init__(self, config_type, global_config):
        super().__init__()
        self.CONFIG_FILE = os.path.join(global_config['config_location'], 
                                   global_config['spectraToolboxView'])
        self.global_config = global_config
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
                widget = class_type(self.config[self.config_type]['widgets'][key], self.global_config)
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

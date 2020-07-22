from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal
import spectraNavigatorWidgets as widgets
from configparser import ConfigParser
import toml
from importlib import import_module
from copy import copy
from collections import OrderedDict as od


class spectraToolboxView(QWidget):
    CONFIG_FILE = "config/toolbox_view.toml"

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
        self.config_type = config_type
        self.config = toml.load(self.CONFIG_FILE)
        self.layout = QVBoxLayout()

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(self.verticalSpacer)

        self.setupWidgets()



        self.setLayout(self.layout)
        self.connectSignals()
        #for k,v in self.outgoingSignals.items():
        #    print(k)
        #    v({"test": 'test'})

    
    def setupWidgets(self):
        self.widgets = {}
        for key, val in self.config['general']['widgets'].items():
            mod = import_module(key)
            for name, obj in val.items():
                if name in self.config[self.config_type]['widgets'].keys():
                    class_type = getattr(mod, obj)
                    widget = class_type(self.config[self.config_type]['widgets'][name])
                    self.widgets.update({name: widget})
                    self.layout.addWidget(widget)
                else:
                    class_type = getattr(mod, obj)
                    widget = class_type()
                    self.widgets.update({name: widget})
                    self.layout.addWidget(widget)



    
    def connectSignals(self):
        for name, widget in self.widgets.items():
            if hasattr(widget, "signal"):
                widget.signal.connect(lambda x, y=name: self.test({y: x}))

if __name__ == "__main__":
    app = QApplication([])
    window = spectraToolboxView("keckode")
    window.show()
    app.exec_()
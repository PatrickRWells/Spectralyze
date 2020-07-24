from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
import toml
from importlib import import_module
import os
from spectralyze.gui.Models.fileModel import fileModel

class abstractSpectraModel(fileModel):
    """
    An abstract class for handling spectra objects
    """
    CONFIG_FILE = os.path.join(os.environ['SPECTRALYZE_CONFIG'],"spectra_model.toml")
    def __init__(self, fname, config_type):
        self.config_type = config_type
        self.config = toml.load(self.CONFIG_FILE)
        self.toolbox = None
        self.fname = fname
        self.attributes = {}
        self.setup()
    
    def getWidget(self):
        """
        Get a QWidget for viewing data
        Should always be implemented specific implementation of this class
        """

    def setup(self):        
        for key, val in self.config[self.config_type]['attributes'].items():
            if self.config[self.config_type]['type'] == 'multi':
                self.attributes.update({key: []})
            else:
                self.attributes.update({key: val})
        
        self.toolbox = self.config[self.config_type]['toolbox']
    

    def update(self, data):
        """
        Should be implemented in the derived class
        Widget needs to be able to handle dictionaries
        Where the key is one of the keys in the toolboxview
        configuration
        """
        pass

    def connectToolbox(self, toolbox):
        self.toolbox = toolbox
        self.toolbox.signal.connect(lambda x: self.update(x))  
        pass


if __name__ == "__main__":
    pass
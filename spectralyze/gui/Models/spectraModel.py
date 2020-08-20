from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
import toml
from importlib import import_module
import os
from spectralyze.gui.Models.fileModel import fileModel
import pickle

class abstractSpectraModel(fileModel):
    """
    An abstract class for handling spectra objects
    """
    def __init__(self, fname, config_type, global_config):
        super().__init__()

        self.global_config = global_config
        self.CONFIG_FILE = os.path.join(self.global_config['config_location'],
                                        self.global_config['spectraModel'])
        self.config_type = config_type
        self.config = toml.load(self.CONFIG_FILE)
        self.toolbox = None
        self.fname = fname
        self.attributes = {}
        self.setup()        
        
    def updateAttributes(self, attributes):
        self.attributes = attributes
        

    def getWidget(self):
        """
        Get a QWidget for viewing data
        Should always be implemented specific implementation of this class
        """

    def setup(self):        
        for key, val in self.config[self.config_type]['attributes'].items():
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

    def forceToolboxUpdate(self):
        pass

    def exportMetaData(self, fpath):
        data = self.attributes
        fname = '.'.join([fpath, 'specm'])
        with open(fname, 'wb') as outfile:
            pickle.dump(data, outfile)

    def importMetaData(self, data):
        for key in data.keys():
            with open(key, 'rb') as infile:
                data = pickle.load(infile)
                self.attributes = data
            self.forceToolboxUpdate()

    def handleSignal(self, signal):
        if hasattr(self,  signal['action']):
            print("Yay!")
            print(self.fileManager)



from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
import toml
from importlib import import_module


class abstractSpectraModel:
    CONFIG_FILE="config/spectra_model.toml"
    def __init__(self, fname, configtype):
        self.configtype = configtype
        self.config = toml.load(self.CONFIG_FILE)
        self.fname = fname
        self.attributes = {}
        self.setup()

    def setup(self):
        for key, val in self.config[self.configtype]['attributes']:
            if self.config[self.configtype]['type'] == 'multi':
                self.attributes.update({key: []})
            else:
                self.attributes.update({key: val})
    
    def plot(self, index=0, **kwargs):
        pass



if __name__ == "__main__":
    pass
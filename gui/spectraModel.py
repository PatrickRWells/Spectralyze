from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from keckcode.deimos import deimosmask1d
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject

class spectraModel:
    def __init__(self, fname):
        self.fname = fname
        self.mask = deimosmask1d.DeimosMask1d(fname)
        self.numspec = self.mask.nspec
        self.zguesses = [0] * self.numspec
    
    def updateZGuess(self, index, zguess):
        self.zguesses[index] = zguess

    def getZGuess(self, index):
        return self.zguesses[index]
    
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['mask']
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.mask = deimosmask1d.DeimosMask1d(self.fname)


class figCanvas(FigureCanvas):
    def __init__(self, figure):
        self.fig = figure
        super().__init__(self.fig)

if __name__ == "__main__":
    pass
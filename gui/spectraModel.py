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
        self.plot = self.mask.plot(0)
    
        self.canvas = figCanvas(self.plot)
        self.zguesses = [0] * self.numspec

    def getPlot(self, index):
        self.plot.clf()
        self.mask.plot(index, fig=self.plot)
        self.canvas.draw()
    
    def getSmoothPlot(self, index, smoothing):
        self.plot.clf()
        self.mask.smooth(index, smoothing, fig=self.plot)
        self.canvas.draw()
    
    def updateZGuess(self, index, zguess):
        self.zguesses[index] = zguess

    def getZGuess(self, index):
        return self.zguesses[index]

    def updateLines(self, lines, specnum, smooth, smoothing):
        print(smooth)
        print(smoothing)
        if smooth:
            self.getSmoothPlot(specnum, smoothing)
        else:
            self.getPlot(specnum)
        
        self.mask.mark_lines(lines, self.zguesses[specnum], specnum, fig=self.plot, usesmooth=smooth)
        self.canvas.draw()

class figCanvas(FigureCanvas):
    def __init__(self, figure):
        self.fig = figure
        super().__init__(self.fig)

if __name__ == "__main__":
    pass
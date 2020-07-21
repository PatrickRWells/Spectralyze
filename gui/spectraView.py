from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
import time


from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSignal

from spectraModel import spectraModel, figCanvas
from keckcode.deimos import deimosmask1d
import sys

class spectraView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.plot = self.model.mask.plot(0)
        print(self.plot)
        
        self.canvas = figCanvas(self.plot)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.toolbar)
        self.setLayout(self.layout)

    def getPlot(self, index):
        self.plot.clf()
        self.model.mask.plot(index, fig=self.plot)
        self.canvas.draw()
        self.repaint()
    
    def getSmoothPlot(self, index, smoothing):
        self.plot.clf()
        self.model.mask[index].smooth(smoothing, fig=self.plot)
        self.canvas.draw()
        self.repaint()

    def updateLines(self, lines, specnum, smooth, smoothing):
        if smooth:
            self.getSmoothPlot(specnum, smoothing)
        else:
            self.getPlot(specnum)
        
        self.model.mask.mark_lines(lines, self.model.zguesses[specnum], specnum, fig=self.plot, usesmooth=smooth)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    fname = "/Volumes/Workspace/Data/reduced/Science/spec1d_d0721_0057-2209m1_DEIMOS_2017Jul21T091032.880.fits"
    SpectraModel = spectraModel(fname)
    window = spectraView(SpectraModel)

    button = QPushButton()
    button.show()
    window.show()

    sys.exit(app.exec_())

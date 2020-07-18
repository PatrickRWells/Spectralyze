from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
import time


from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSignal

from spectraModel import spectraModel
from keckcode.deimos import deimosmask1d
import sys

class spectraView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.canvas = self.model.canvas

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.toolbar)
        self.setLayout(self.layout)

    def plot(self, index):
        self.model.getPlot(index)
        self.canvas.draw()
        self.repaint()
    
    def smoothSpectra(self, index, smoothing):
        self.model.getSmoothPlot(index, smoothing)
        self.canvas.draw()
        self.repaint()

if __name__ == "__main__":
    app = QApplication([])
    fname = "/Volumes/Workspace/Data/reduced/Science/spec1d_d0721_0057-2209m1_DEIMOS_2017Jul21T091032.880.fits"
    SpectraModel = spectraModel(fname)
    window = spectraView(SpectraModel)

    button = QPushButton()
    button.show()
    window.show()

    sys.exit(app.exec_())

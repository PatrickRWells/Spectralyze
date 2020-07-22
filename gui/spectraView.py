from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
import time


from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSignal
from keckcode.deimos import deimosmask1d
import sys

class spectraView(QWidget):
    """
    Widget for displaying a spectra

    Methods:
        getPlot(int): Draws a plot at the given index
        getSmoothPlot(int, int): Gets plot at given index
                                 with smoothing by second value
        updateLines(lines, specnum, smooth, smoothing)
            Draws spectral lines on a given plot

            lines: dictionary with entries {lineid: bool}
            specnum: spectra to draw the line on (index)
            smoothing: amount of smoothing, 0 for none

    Attributes:
        model: spectra model object
        plot: displayed plot, reused to redraw
        canvas: UI element for holding plot
        toolbar: Toolbar UI for plot interaction


    """

    def __init__(self, model):
        super().__init__()
        self.model = model
        
        self.plot = self.model.mask.plot(0)
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

    def updateLines(self, lines, specnum, smoothing=0):
        
        if smoothing != 0:
            self.getSmoothPlot(specnum, smoothing)
        else:
            self.getPlot(specnum)
        
        #Note: Plot is cleared and past back to plotting library for reuse
        self.model.mask.mark_lines(lines, self.model.zguesses[specnum], specnum, fig=self.plot, usesmooth=bool(smoothing))
        self.canvas.draw()


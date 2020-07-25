from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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

    def __init__(self, plot):
        super().__init__()
        self.plot = plot
        self.canvas = figCanvas(self.plot)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.toolbar)
        self.setLayout(self.layout)

class figCanvas(FigureCanvas):
    def __init__(self, figure):
        self.fig = figure
        super().__init__(self.fig)
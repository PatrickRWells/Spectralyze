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
    Widget for displaying a spectra plot
    Doesn't actually know anything about how the plot works
    Just displays it

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

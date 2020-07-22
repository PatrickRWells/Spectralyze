    
from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSizePolicy, QLabel
from PyQt5 import QtCore
from spectraModelWrappers import deimos1DSpectra
from spectraToolboxView import spectraToolboxView
import sys
from time import sleep
import toml

class spectraNavigatorView(QWidget):
    CONFIG_FILE = "config/spectra_view.toml"
    def __init__(self, model, config_type):
        self.config_type = config_type
        self.toolboxView = spectraToolboxView(self.config_type)


    


if __name__ == "__main__":

    app = QApplication([])
    fname = "/Volumes/Workspace/Data/reduced/Science/spec1d_d0721_0057-2209m1_DEIMOS_2017Jul21T091032.880.fits"
    SpectraModel = deimos1DSpectra(fname)

    SpectraNavigatorView = spectraNavigatorView(SpectraModel, "keckode")
    SpectraNavigatorView.show()
    
    app.exec_()

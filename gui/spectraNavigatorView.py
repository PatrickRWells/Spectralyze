    
from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSizePolicy, QLabel
from PyQt5 import QtCore
from spectraView import spectraView
from spectraModel import spectraModel
from spectraToolboxView import spectraToolboxView
import sys
from time import sleep

class spectraNavigatorView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.spectraView = spectraView(self.model)
        self.toolbox = spectraToolboxView()
        self.layout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()

        


        self.nspec = self.model.numspec
        self.curspec = 0
        self.issmoothed = False
        self.cursmooth = 0
        
        self.spectraLabel = QLabel("")
        self.updateSpectraLabel()
        self.spectraLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.leftLayout.addWidget(self.spectraLabel)
        self.leftLayout.addWidget(self.spectraView)
        self.layout.addLayout(self.leftLayout)

        self.layout.addWidget(self.toolbox)

        self.spectraView.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.setLayout(self.layout)
        self.spectraView.show()

        self.connectSlots()
    
    def connectSlots(self):
        self.toolbox.nextPressed.connect(self.nextPlot)
        self.toolbox.prevPressed.connect(self.prevPlot)
        self.toolbox.smoothPressed.connect(lambda x: self.smoothSpectra(x))
        self.toolbox.undoSmoothPressed.connect(self.undoSmooth)
        self.toolbox.zGuessInput.connect(lambda x: self.zGuessChanged(x))
        self.toolbox.spectralLineTool.linesUpdate.connect(lambda x: self.updateLines(x))
    

    def nextPlot(self):
        self.curspec += 1
        self.spectraView.getPlot(self.curspec)
        self.toolbox.setZ(self.model.getZGuess(self.curspec))
        self.issmoothed = False
        self.updateSpectraLabel()

    def prevPlot(self):
        self.curspec -= 1
        self.toolbox.setZ(self.model.getZGuess(self.curspec))
        self.spectraView.getPlot(self.curspec)
        self.issmoothed = False
        self.updateSpectraLabel()

    def smoothSpectra(self, smoothing):
        self.spectraView.getSmoothPlot(self.curspec, smoothing)
        self.issmoothed = True
        self.cursmooth = smoothing

    def undoSmooth(self):
        self.spectraView.getPlot(self.curspec)
        self.issmoothed = False
        self.cursmooth = 0

    def zGuessChanged(self, zguess):
        self.model.updateZGuess(self.curspec, zguess)
    
    def updateLines(self, lines):
        self.spectraView.updateLines(lines, self.curspec, smooth=self.issmoothed, smoothing=self.cursmooth)

    def updateSpectraLabel(self):
        text = "Spectrum {} of {}".format(self.curspec, self.nspec)
        self.spectraLabel.setText(text)
        self.spectraLabel.repaint()


if __name__ == "__main__":

    app = QApplication([])
    fname = "/Volumes/Workspace/Data/reduced/Science/spec1d_d0721_0057-2209m1_DEIMOS_2017Jul21T091032.880.fits"
    SpectraModel = spectraModel(fname)
    SpectraNavigatorView = spectraNavigatorView(SpectraModel)
    SpectraNavigatorView.show()
    
    app.exec_()

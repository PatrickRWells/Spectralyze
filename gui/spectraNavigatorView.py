    
from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from spectraView import spectraView
from spectraModel import spectraModel
from spectraNavigatorModel import spectraNavigatorModel
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
        self.layout.addWidget(self.spectraView)
        self.layout.addWidget(self.toolbox)
        self.setLayout(self.layout)


        self.nspec = self.model.numspec
        self.curspec = 0
        self.issmoothed = False
        self.cursmooth = 0
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
        self.spectraView.plot(self.curspec)
        self.toolbox.setZ(self.model.getZGuess(self.curspec))
        self.issmoothed = False

    def prevPlot(self):
        self.curspec -= 1
        self.toolbox.setZ(self.model.getZGuess(self.curspec))
        self.spectraView.plot(self.curspec)
        self.issmoothed = False

    def smoothSpectra(self, smoothing):
        self.spectraView.smoothSpectra(self.curspec, smoothing)
        self.issmoothed = True
        self.cursmooth = smoothing

    def undoSmooth(self):
        self.spectraView.plot(self.curspec)
        self.issmoothed = False
        self.cursmooth = 0

    def zGuessChanged(self, zguess):
        self.model.updateZGuess(self.curspec, zguess)
    
    def updateLines(self, lines):
        self.model.updateLines(lines, self.curspec, smooth=self.issmoothed, smoothing=self.cursmooth)


if __name__ == "__main__":

    app = QApplication([])
    fname = "/Volumes/Workspace/Data/reduced/Science/spec1d_d0721_0057-2209m1_DEIMOS_2017Jul21T091032.880.fits"
    SpectraModel = spectraModel(fname)
    SpectraNavigatorView = spectraNavigatorView(SpectraModel)
    SpectraNavigatorView.show()
    
    app.exec_()


from keckcode.deimos import deimosmask1d
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from project import Project

class plotHandler(QApplication):
    def __init__(self, fname, remote):
        self.project = Project()
        self.remote = remote
        plt.ion()
        self.mask = deimosmask1d.DeimosMask1d(fname)
        self.nspec = self.mask.nspec
        self.currspec = 0
        self.currSmoothing = 0
        self.currSmooth = False
        self.project.addSpecFile(fname, self.nspec)
        self.fname = fname
        self.mask.plot(0)
        
        
        self.connectSignals()

    def connectSignals(self):
        self.remote.goNext.connect(lambda: self.go_next())
        self.remote.goPrev.connect(lambda: self.go_previous())
        self.remote.goSmooth.connect(lambda x: self.smooth(x))
        self.remote.goUndoSmooth.connect(lambda: self.undoSmooth())
        self.remote.goZGuess.connect(lambda x: self.addZGuess(x))
        self.remote.goUpdateSpectra.connect(lambda x: self.updateSpectra(x))
    
    def go_next(self):
        if self.currspec < self.nspec-1:
            self.currspec += 1
            plt.clf()
            self.mask.plot(self.currspec)
            self.remote.updateZ(self.getZGuess())
            self.currSmooth = False
            self.currSmoothing = 0
    
    def go_previous(self):
        if self.currspec > 0:
            self.currspec -= 1
            plt.clf()
            self.mask.plot(self.currspec)
            self.remote.updateZ(self.getZGuess())
            self.currSmooth = False
            self.currSmoothing = 0

    def smooth(self, smoothing):
        plt.clf()
        self.mask.smooth(self.currspec, smoothing)
        self.currSmooth = True
        self.currSmoothing = smoothing

    def undoSmooth(self):
        if self.currSmooth:
            self.currSmooth = False
            plt.clf()
            self.mask.plot(self.currspec)

    def addZGuess(self, zGuess):
        self.project.addZGuess(self.fname, self.currspec, zGuess)

    def getZGuess(self):
        return self.project.getZGuess(self.fname, self.currspec)

    def updateSpectra(self, spectra):
        plt.clf()
        if self.currSmooth:
            self.mask.smooth(self.currspec, self.currSmoothing)
        else:
            self.mask.plot(self.currspec)
        for k, v in spectra.items():
            if v == 2:
                self.mask[self.currspec].mark_lines(k, self.project.getZGuess(self.fname, self.currspec))



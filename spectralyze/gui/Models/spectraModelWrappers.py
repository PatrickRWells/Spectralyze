from keckcode.deimos import deimosmask1d
from spectralyze.gui.Models.spectraModel import abstractSpectraModel
from spectralyze.gui.Views.spectraView import spectraView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5 import QtCore
import os
import toml
from importlib import import_module

"""
Conains wrappers for various backends for data display and management
class needs to be included in the appropriate entry in the various config
files for the code to be able to use it.



"""


class deimos1DSpectra(abstractSpectraModel):
    """
    1D Deimos spectra, as implemented in:
    https://github.com/cdfassnacht/keckcode
    """
    def __init__(self, fname):
        super().__init__(fname, "keckcode_deimos1d")
        self.mask = deimosmask1d.DeimosMask1d(self.fname)
        self.keys = list(self.mask.keys())
        self.plot = self.mask.plot(self.keys[0])
        self.nspec = self.mask.nspec
        self.curspec = 0
        self.cursmooth = 0
        self.attributes['zguess'] = self.nspec*[0.0]

    def update(self, data):
        for key, value in data.items():
            if key == 'navigator':
                if value == 'next':
                    self.nextGraph()
                if value == "previous":
                    self.prevGraph()
            elif key == "smoothing":
                self.smoothGraph(value)
            elif key == "lineupdate":
                self.updateLines(value)
            elif key == "zguess":
                self.zGuessUpdate(value)


    def getWidget(self):
        self.widget = QWidget()
        self.widget_layout = QVBoxLayout()
        self.label = QLabel("Spectra {} out of {}".format(self.curspec+1, self.nspec))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.spectraView = spectraView(self.plot)
        self.widget_layout.addWidget(self.label)
        self.widget_layout.addWidget(self.spectraView)
        self.widget.setLayout(self.widget_layout)

        self.widgetHeight = 600
        self.widgetWidth = 800
        self.widget.setMinimumSize(self.widgetWidth, self.widgetHeight)

        return self.widget

    def updateLabel(self):
        self.label.setText("Spectra {} out of {}".format(self.curspec + 1, self.nspec))


    def plotGraph(self, index):
        self.plot.clf()
        self.mask.plot(self.keys[index], fig=self.plot)
        self.spectraView.canvas.draw()
        self.updateLabel()
        self.widget.repaint()

    def nextGraph(self, **kwargs):
        if self.curspec < self.nspec - 1:
            self.curspec += 1
            self.plotGraph(self.curspec)
            self.cursmooth = 0
            self.toolbox.update({'zguess': self.attributes['zguess'][self.curspec]})

    def prevGraph(self, **kwargs):
        if self.curspec > 0:
            self.curspec -= 1
            self.plotGraph(self.curspec)
            self.cursmooth = 0
            self.toolbox.update({'zguess': self.attributes['zguess'][self.curspec]})

    def smoothGraph(self, smoothing):
        self.cursmooth = smoothing
        if smoothing == 0:
            self.plotGraph(self.curspec)
        else:
            self.plot.clf()
            self.mask.smooth(self.keys[self.curspec], smoothing, fig=self.plot)
            self.spectraView.canvas.draw()
            self.widget.repaint()

    def updateLines(self, lines):
        if bool(self.cursmooth):
            self.smoothGraph(self.cursmooth)
        else:
            self.plotGraph(self.curspec)

        self.mask.mark_lines(self.keys[self.curspec], self.attributes['zguess'][self.curspec], lines, fig=self.plot, usesmooth=self.cursmooth)
        self.spectraView.canvas.draw()

    def zGuessUpdate(self, zguess, **kwargs):
        self.attributes['zguess'][self.curspec] = zguess


    def __getstate__(self):
        state = self.__dict__.copy()
        del state['mask']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.mask = deimosmask1d.DeimosMask1d(self.fname)


def getSpectraModel(fname, config_type):
    config = toml.load(os.path.join(os.environ['SPECTRALYZE_CONFIG'], 'model_getters.toml'))
    mod = import_module('spectralyze.gui.Models.spectraModelWrappers')
    atr = getattr(mod, config[config_type]['obj'])
    return(atr(fname))

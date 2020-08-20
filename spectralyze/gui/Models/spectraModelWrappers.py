from keckcode.deimos import deimosmask1d
from spectralyze.gui.Models.spectraModel import abstractSpectraModel
from spectralyze.gui.Views.spectraView import spectraView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5 import QtCore
import os
import toml
from importlib import import_module
import matplotlib.pyplot as plt
from spectralyze.utils.modeling import spectraModeler

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
    def __init__(self, fname, global_config):
        super().__init__(fname, "keckcode_deimos1d", global_config)
        self.mask = deimosmask1d.DeimosMask1d(self.fname)
        self.keys = list(self.mask.keys())
        self.plot = plt.figure(dpi=75)
        self.plot = self.mask.plot(self.keys[0], fig=self.plot)
        self.nspec = self.mask.nspec
        self.curspec = 0
        self.cursmooth = 0
        self.attributes = {key: {'zguess': 0, 'confidence': '', 'classification': ''} for key in self.keys}
        self.lines = {}
    
    def update(self, data):
        for key, value in data.items():
            if key == 'navigator':
                self.navigate(value)
            elif key == "smoothing":
                self.smoothGraph(value)
            elif key == "lineupdate":
                self.updateLines(value)
            elif key == "zguess":
                self.zGuessUpdate(value)
            elif key == "classifier":
                self.classificationUpdate(value)
    
    def navigate(self, data):
        for key, val in data.items():
            if key == 'increment':
                if val == 'next':
                    self.nextGraph()
                else:
                    self.prevGraph()
            elif key == 'jump':
                self.plotGraph(val)
            
    def getWidget(self):
        self.widget = QWidget()
        self.widget_layout = QVBoxLayout()
        self.label = QLabel("Spectra {} out of {}".format(self.curspec+1, self.nspec))
        self.label.setMaximumHeight(20)
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
        self.curspec = index
        self.plot.clf()
        self.mask.plot(self.keys[index], fig=self.plot)
        self.spectraView.canvas.draw()
        self.updateLabel()
        self.widget.repaint()
        self.cursmooth = 0

    def nextGraph(self, **kwargs):
        if self.curspec < self.nspec - 1:
            self.curspec += 1
            self.plotGraph(self.curspec)
            self.cursmooth = 0
            self.forceToolboxUpdate()

    def prevGraph(self, **kwargs):
        if self.curspec > 0:
            self.curspec -= 1
            self.plotGraph(self.curspec)
            self.cursmooth = 0
            self.forceToolboxUpdate()

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

        self.mask.mark_lines(lines, self.attributes[self.keys[self.curspec]]['zguess'], self.keys[self.curspec], fig=self.plot, usesmooth=self.cursmooth)
        self.spectraView.canvas.draw()

    def zGuessUpdate(self, zguess, **kwargs):
        skey = self.keys[self.curspec]
        for key,value in zguess.items():
            if key == "guess":
                self.attributes[skey]['zguess'] = value
            elif key == "confidence":
                self.attributes[skey]['confidence'] = value

    def classificationUpdate(self, classification):
        for key, val in classification.items():
            if key == 'classification':
                skey = self.keys[self.curspec]
                self.attributes[skey]['classification'] = val

    def forceToolboxUpdate(self):
        key = self.keys[self.curspec]
        self.toolbox.update({'zguess': {'zguess': self.attributes[key]['zguess']}})
        self.toolbox.update({'zguess': {'confidence': self.attributes[key]['confidence']}})
        self.toolbox.update({'navigator':{'nspec': self.nspec}})
        self.toolbox.update({'lineupdate': {'strongem' : False, 'em' : False, 'abs' : False}})
        self.toolbox.update({'spectraInfo':{'slitid': self.getCurrentSlitId()}})
        self.toolbox.update({'classifier': {'classification': self.attributes[key]['classification']}})
    
    def getCurrentSlitId(self):
        name = self.keys[self.curspec]
        slit = name.split('_')[1]
        return slit



def getSpectraModel(fname, config_type, global_config):
    config_location = os.path.join(global_config['config_location'],
                                    global_config['getSpectraModel'])
    config = toml.load(config_location)
    mod = import_module('spectralyze.gui.Models.spectraModelWrappers')
    atr = getattr(mod, config[config_type]['obj'])
    return(atr(fname, global_config))

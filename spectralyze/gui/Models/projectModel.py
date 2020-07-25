from spectralyze.gui.Models.fileModel import getFileModel
from PyQt5.QtWidgets import QStackedWidget
import pickle
import os
import toml
from importlib import import_module

class projectModel:
    CONFIG_FILE = os.path.join(os.environ['SPECTRALYZE_CONFIG'], "project_models.toml")
    def __init__(self, name):
        super().__init__()
        self.fileModels = {}
        self.fileWidgets = {}
        self.fileConfigs = {}
        self.config = toml.load(self.CONFIG_FILE)
        self.widget = None
        self.saveLocation = ""
        self.name = name

    def addFile(self, fname, config_type):
        if fname in self.fileModels.keys():
            pass
        else:
            self.fileModels.update({fname: getFileModel(fname, 'spectra', config_type)})
            self.fileConfigs.update({fname: config_type})
            if self.widget:
                self.updateWidget()
    
    def removeFile(self, fname):
        if fname in self.fileModels.keys():
            model = self.fileModels.pop(fname)
            self.fileConfigs.pop(fname)
            self.updateWidget(remove=fname)
            del model
        

    def getFileNames(self):
        return self.fileModels.keys()
    
    def getFileModel(self, fname):
        if fname in self.fileModels.keys():
            return self.fileModels[fname]

    def saveProjectModel(self, fname):
        self.saveLocation = fname
        pickle.dump(self, self.saveLocation)
    
    def getWidget(self):
        self.widget = QStackedWidget()
        for fname, model in self.fileModels.items():
            widget = self.getFileWidget(fname)
            self.fileWidgets.update({fname: widget})
            self.widget.addWidget(widget)
        return self.widget
    
    def updateWidget(self, remove = None):
        if remove:
            widget = self.fileWidgets.pop(remove)
            self.widget.remove(widget)
            if self.fileWidgets.keys():
                self.setActive(list(self.fileWidgets.keys())[0])
            del widget


        for fname, model in self.fileModels.items():
            if fname not in self.fileWidgets.keys():
                widget = self.getFileWidget(fname)
                self.fileWidgets.update({fname: widget})
                self.widget.addWidget(widget)
                self.widget.update()
            

    
    def setActive(self, fname):
        for key, val in self.fileWidgets.items():
            if fname in key:
                self.widget.setCurrentWidget(self.fileWidgets[key])
                break
            
    def getFileWidget(self, fname):
        config_type = self.fileConfigs[fname]
        module = import_module(self.config['widgets'][config_type]['mod'])
        obj = getattr(module, self.config['widgets'][config_type]['obj'])
        return obj(self.fileModels[fname], self.fileConfigs[fname])

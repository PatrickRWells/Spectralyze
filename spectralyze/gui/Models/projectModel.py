from spectralyze.gui.Models.fileModel import getFileModel
from PyQt5.QtWidgets import QStackedWidget
import pickle
import os
import toml
from importlib import import_module
from copy import copy

class projectModel:
    def __init__(self, name, global_config, file_manager):
        super().__init__()
        self.fileManager = file_manager
        self.global_config = global_config
        self.CONFIG_FILE = os.path.join(self.global_config['config_location'], 
                                        self.global_config['projectModel'])
        self.fileModels = {}
        self.fileWidgets = {}
        self.fileConfigs = {}
        self.config = toml.load(self.CONFIG_FILE)
        self.widget = None
        self.saveLocation = ""
        self.name = name
    
    def setFileManager(self, f):
        self.fileManager = f

    def __getstate__(self):

        data = copy(self.__dict__)
        del data['fileManager']
        del data['widget']
        del data['fileWidgets']
        attributes = {}
        for k, v in data['fileModels'].items():
            attributes.update({k: v.attributes})
        del data['fileModels']
        data.update({'attributes': attributes})
        return data
    
    def __setstate__(self, state):
        attributes = state.pop('attributes')
        self.__dict__ = state
        self.fileWidgets = {}
        self.fileModels = {}
        self.widget = None
        for fname, configtype in self.fileConfigs.items():
            self.addFile(fname, configtype)
            self.fileModels[fname].attributes = attributes[fname]





    def addFile(self, fname, config_type):
        if fname in self.fileModels.keys():
            pass
        else:
            self.fileModels.update({fname: getFileModel(fname, 'spectra', config_type, self.global_config)})
            self.fileConfigs.update({fname: config_type})
            if self.widget is not None:
                self.updateWidget()
            else:
                pass

    def removeFile(self, fname):
        for filename in self.fileModels.keys():
            if fname in filename:
                model = self.fileModels.pop(filename)
                self.fileConfigs.pop(filename)
                self.updateWidget(remove=filename)
                del model
                break
            

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
            self.widget.removeWidget(widget)
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
        return obj(self.fileModels[fname], self.fileConfigs[fname], self.global_config)

    def save(self):
        self.fileManager.saveProject(self)
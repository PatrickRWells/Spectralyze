from spectralyze.gui.Models.fileModel import getFileModel
from PyQt5.QtWidgets import QStackedWidget, QFileDialog
from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSignal, QObject
from spectralyze.gui.Views.fileBrowse import fileBrowser
import pickle
import os
import toml
from importlib import import_module
from copy import copy
import time

threadPool = QThreadPool()

class projectModel(QObject):
    """
    Model for storing and retrieving project data.
    attributes
    ----------
    fileManager: File manager for saving data to disk
    fileModels: Individual file models. Type will depend on kind of file
    fileWidgets: References to the UI widgets associated with the files
    fileConfigs: Dictionary containing file types    
    """
    loadingComplete = pyqtSignal()
    def __init__(self, name, global_config, file_manager):
        super().__init__()
        self.fileManager = file_manager
        self.global_config = global_config
        self.fileModels = {}
        self.fileWidgets = {}
        self.fileConfigs = {}
        self.loaded = {}
        self.active = None
        self.getConfig()
        self.widget = None
        self.saveLocation = ""
        self.name = name

    def getConfig(self):
        self.CONFIG_FILE = os.path.join(self.global_config['config_location'], 
                                        self.global_config['projectModel'])
        self.config = toml.load(self.CONFIG_FILE)


    def updateGlobalConfig(self, config):
        self.global_config = config
        for fmodel in self.fileModels.values():
            fmodel.updateGlobalConfig(config)
    def setFileManager(self, f):
        """
        Used when loading a previously saved project
        """
        self.fileManager = f
        for model in self.fileModels.values():
            model.setFileManager(f)

    def __getstate__(self):
        """
        Prepare project data for disk storage.
        References to UI, and other things that are stateless are removed
        """
        data = copy(self.__dict__)
        del data['fileManager']
        del data['widget']
        del data['fileWidgets']
        del data['config']
        attributes = {}
        for k, v in data['fileModels'].items():
            att = v.attributes
            attributes.update({k: att})
        del data['fileModels']
        data.update({'attributes': attributes})
        return data
    
    def __setstate__(self, state):
        """
        Reads in the data as outputted by __getstate___
        Automatically called when the project is opened
        """
        super().__init__()
        attributes = state.pop('attributes')
        self.__dict__ = state
        self.fileWidgets = {}
        self.fileModels = {}
        self.loaded = {}
        self.widget = None
        self.getConfig()

        for fname, configtype in self.fileConfigs.items():
            self.addFile(fname, configtype, attributes[fname])
        
    def setVersion(self, vnumber):
        self.version = vnumber

    def addFile(self, fname, config_type, attributes={}):
        """
        Adds a file to the project. 
        fname: absolute path to the file
        config_type: one of the config types from 
        """
        if fname in self.fileModels.keys():
            pass
        else:
            self.fileConfigs.update({fname: config_type})
            loader = fileLoader(fname, config_type, self.global_config, attributes)
            loader.signals.result.connect(lambda x: self.updateFiles(x))
            threadPool.start(loader)

    def updateFiles(self, fileobj):
        self.fileModels.update({fileobj.fname: fileobj})
        fileobj.updateGlobalConfig(self.global_config)
        self.loaded.update({fileobj.fname: True})
        if self.widget is not None:
            self.updateWidget()
        
        if len(self.fileModels.keys()) > 0:
            self.active = list(self.fileModels.keys())[-1]

        if len(self.loaded) == len(self.fileConfigs.keys()):
            self.loadingComplete.emit()


    def removeFile(self, fname):
        """
        Removes a file from the project
        """
        for filename in self.fileModels.keys():
            if fname in filename:
                model = self.fileModels.pop(filename)
                self.fileConfigs.pop(filename)
                self.updateWidget(remove=filename)
                del model
                break
            

    def getFileNames(self):
        return self.fileConfigs.keys()
    
    def getFileConfigs(self):
        return self.fileConfigs
        
    def getFileModel(self, fname):
        if fname in self.fileModels.keys():
            return self.fileModels[fname]
    
    def getWidget(self):
        """
        Gets a UI widget for a project.
        Presently, this is just a stack of the widgets associated
        with the various files
        """

        self.widget = QStackedWidget()
        for fname, model in self.fileModels.items():
            widget = self.getFileWidget(fname)
            self.fileWidgets.update({fname: widget})
            self.widget.addWidget(widget)
        return self.widget
    
    def updateWidget(self, remove = None):
        """
        Updates the widget. If no name is passed, checks
        for new file models and adds their widget if found.
        If a name is passed, removes that widget from the stack
        """
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
        """
        Sets the active widget (i.e. top of the stack)
        """
        for key, val in self.fileWidgets.items():
            if fname in key:
                self.widget.setCurrentWidget(self.fileWidgets[key])
                self.active = fname
                break
            
    def getFileWidget(self, fname):
        """
        Get UI widget for a particular file. 
        """
        config_type = self.fileConfigs[fname]
        module = import_module(self.config['widgets'][config_type]['mod'])
        obj = getattr(module, self.config['widgets'][config_type]['obj'])
        return obj(self.fileModels[fname], self.fileConfigs[fname], self.global_config)

    def save(self):
        """
        Sends itself to the file manager to be saved
        """
        self.fileManager.saveProject(self)
    
    def canHandle(self, target):
        """
        Checks if this object can handle a signal aimed at a particular target
        """
        if target in self.config['signals']['canHandle']:
            return True
        else:
            return False
    
    def handleSignal(self, signal):
        if signal['target'] == 'fileModel':
            self.fileModels[self.active].handleSignal(signal)

    def exportData(self, fname, dtype):
        for key, val in self.fileModels.items():
            if fname in key:
                name = QFileDialog.getSaveFileName()
                val.exportFileData(name[0])
    
    def importData(self, fname, data, dtype):
        for key, val in self.fileModels.items():
            if fname in key:
                browser = fileBrowser("spectra meta") #Currently this is the only type of file
                browser.fileOpened.connect(lambda x: val.importFileData(x))
                browser.openFile()
    

class fileLoader(QRunnable):
    def __init__(self, file, config_type, global_config, attributes = {}):
        super().__init__()
        self.file = file
        self.config_type = config_type
        self.global_config = global_config
        self.signals = signals()
        self.attributes = attributes

    def run(self):
        data = getFileModel(self.file, 'spectra', self.config_type, self.global_config)
        if self.attributes:
            data.updateAttributes(self.attributes)
        
        self.signals.result.emit(data)

class signals(QObject):
    result=pyqtSignal(object)
    def __init__(self):
        super().__init__()


class projectLoader(QObject):
    loadingComplete = pyqtSignal(object)
    def __init__(self, fname, fileManager):
        super().__init__()
        self.fname = fname
        self.fileManager = fileManager
        self.signals = signals()
    
    def loadProject(self):
        with open(self.fname, 'rb') as f:
            project = pickle.load(f)
            project.setFileManager(self.fileManager)
            project.loadingComplete.connect(lambda x=project: self.complete(x))

    def complete(self, project):
        project.setFileManager(self.fileManager)
        self.loadingComplete.emit(project)



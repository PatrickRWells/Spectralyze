from pathlib import Path
import os
import pickle
import toml
from PyQt5.QtCore import QThreadPool, pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog
from spectralyze.gui.Models.projectModel import projectLoader
import signal

class fileManager(QObject):
    projectLoadComplete = pyqtSignal(dict)
    PROJECT_SAVE_LOCATION = os.path.join(str(Path.home()), '.spectralyze')
    PROJECT_CONFIG_LOCATION = os.path.join(PROJECT_SAVE_LOCATION, 'projects.toml')
    def __init__(self):
        super().__init__()
        self.checkSaveDir()
        self.checkSaveConfig()
        self.projects = toml.load(self.PROJECT_CONFIG_LOCATION)
        self.threadPool = QThreadPool()

    def saveProject(self, model):
        filename = os.path.join(self.PROJECT_SAVE_LOCATION, '.'.join([model.name, 'spec']))
        self.updateProjects(model.name, filename)
        with open(filename, 'wb') as projectfile:
            pickle.dump(model, projectfile)
    
    def openProject(self, name):
        filename = self.projects[name]
        loader = projectLoader(filename, self)
        loader.loadingComplete.connect(lambda x, y = name: self.doneLoading(y, x))
        loader.loadProject()
    
    def doneLoading(self, name, obj):
        self.projectLoadComplete.emit({'name': name, 'obj': obj})
    
    def removeProject(self, name):
        if name in self.projects.keys():
            filename = self.projects[name]
            os.remove(filename)
            self.projects.pop(name)
            with open(self.PROJECT_CONFIG_LOCATION, 'w') as f:
                toml.dump(self.projects, f)

    def checkSaveDir(self):
        if not os.path.exists(self.PROJECT_SAVE_LOCATION):
            os.mkdir(self.PROJECT_SAVE_LOCATION)
    
    def checkSaveConfig(self):
        if not os.path.exists(self.PROJECT_CONFIG_LOCATION):
            file = open(self.PROJECT_CONFIG_LOCATION, 'w')
            file.close()
    
    def updateProjects(self, name, fname):
        self.projects.update({name: fname})
        with open(self.PROJECT_CONFIG_LOCATION, 'w') as file:
            toml.dump(self.projects, file)

    def getSavedProjects(self):
        return self.projects.keys()



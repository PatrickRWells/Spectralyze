
from PyQt5.QtWidgets import QApplication
import spectralyze
from spectralyze.gui.Views.startupView import startupView
from spectralyze.gui.Controllers.fileManager import fileManager
from spectralyze.gui.Models.projectModel import projectModel
from spectralyze.gui.Views.projectView import projectView
import os
import toml
import atexit


class spectralyzeApp(QApplication):
    global_config = os.path.join(os.path.dirname(os.path.abspath(spectralyze.__file__)), 
                                'gui/config/')
    resources = os.path.join(os.path.dirname(os.path.abspath(spectralyze.__file__)), 
                                'gui/resources/')

    def __init__(self):
        super().__init__([])
        self.config_location = os.path.join(self.global_config, 'master_config.toml')
        self.config = toml.load(self.config_location)
        self.config['config_location'] = self.global_config
        self.config['resource_location'] = self.resources
        self.fileManager =  fileManager()
        self.activeWindow = startupView(global_config=self.config_location,
                                        file_manager=self.fileManager)
        self.windows = {}
        self.projects = {}
        self.windows.update({'startup': self.activeWindow})
        atexit.register(self.shutdown)
        self.connectSlots()

    def startup(self):
        self.activeWindow.show()
    
    def shutdown(self):
        with open(self.config_location, 'w') as file:
            toml.dump(self.config, file)
    
    def connectSlots(self):
        self.windows['startup'].addProject.connect(lambda x: self.newProject(x))
        self.windows['startup'].openSavedProject.connect(lambda x: self.openProject(x))
        self.windows['startup'].removeSavedProject.connect(lambda x: self.removeProject(x))


    def newProject(self, name):
        project = projectModel(name, self.config, self.fileManager)
        window = projectView(project, self.config)
        self.projects.update({name: project})
        self.windows.update({name: window})
        self.setActiveWindow(window)
        window.saveProject.connect(project.save)
    
    def openProject(self, name):
        project = self.fileManager.openProject(name)
        window = projectView(project, self.config)
        self.projects.update({name: project})
        self.windows.update({name: window})
        self.setActiveWindow(window)
        window.saveProject.connect(project.save)
    
    def removeProject(self, name):
        self.fileManager.removeProject(name)
    
    def setActiveWindow(self, window):
        self.activeWindow.hide()
        self.activeWindow = window
        self.activeWindow.show()

def launch_gui():
    app = spectralyzeApp()
    app.startup()
    app.exec_()


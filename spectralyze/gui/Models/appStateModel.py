from PyQt5.QtWidgets import QApplication
from projectModel import projectModel
from projectView import projectView
from startupView import startupView
import pickle
import os
import configparser

class appStateModel(QApplication):
    def __init__(self):
        super().__init__([])
        self.projectFolder = os.path.join(os.path.expanduser("~"), ".spectralyze")
        self.configPath = os.path.join(self.projectFolder, 'projects.config')

        if not os.path.exists(self.projectFolder):
            os.mkdir(self.projectFolder)
        
        if not os.path.exists(self.configPath):
            file = open(self.configPath, "w")
            config = configparser.ConfigParser()
            config.add_section('Projects')
            config.write(file)
            file.close()

        self.projects = configparser.ConfigParser()
        self.projects.read(self.configPath)
        self.startupView = startupView(self.projects['Projects'].keys())
        self.projectViews = {}
        self.projectModels = {}
        self.startupView.show()
        self.connectSlots()

    def connectSlots(self):
        self.startupView.addProject.connect(lambda x: self.createProject(x))
        self.startupView.openSavedProject.connect(lambda x: self.openSavedProject(x))
        self.startupView.removeSavedProject.connect(lambda x: self.removeSavedProject(x))
        for k, view in self.projectViews.items():
            view.saveProject.connect(lambda x: self.saveProject(x))
        

    def createProject(self, name):
        project = projectModel(name)
        self.projectModels.update({project.name: project})
        self.projectViews.update({project.name: projectView(self.projectModels[project.name])})
        self.projectViews[name].saveProject.connect(lambda x: self.saveProject(x))
        self.startupView.hide()
        self.projectViews[name].show()
        
    
    def addSavedProject(self, fname):
        fpath = os.path.join(self.projectFolder, fname)
        project = pickle.load(open(fpath, 'rb'))
        self.projectModels.update({project.name: project})
        self.projectViews.update({project.name: projectView(self.projectModels[project.name])})
        self.projectViews[project.name].saveProject.connect(lambda x: self.saveProject(x))
    
    
    def showProjectview(self, file):
        self.projectViews[file].show()

    def saveProject(self, project):
        fname = '.'.join([project.strip(' '), 'spf'])
        self.projects.set('Projects', project, fname)
        with open(self.configPath, 'w') as file:
            self.projects.write(file)
        pickle.dump(self.projectModels[project], open(os.path.join(self.projectFolder, fname), 'wb'))
    
    def openSavedProject(self, projectname):
        for project, fname in self.projects['Projects'].items():
            if project == projectname:
                self.addSavedProject(fname)
        self.projectViews[projectname].show()

    def removeSavedProject(self, projectname):
        if projectname in self.projects['Projects'].keys():
            fname = os.path.join(self.projectFolder, self.projects['Projects'][projectname])
            print(fname)
            self.projects.remove_option('Projects', projectname)
            os.remove(fname)
            self.updateProjectsFile()
    
    def updateProjectsFile(self):
        with open(self.configPath, 'w') as file:
            self.projects.write(file)

if __name__ == "__main__":
    app = appStateModel()
    app.exec_()

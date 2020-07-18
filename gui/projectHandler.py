from projectWindow import projectWindow
from editorHandler import editorHandler
from project import Project
from select_data import fileBrowser
from astropy.io import fits
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject

class projectHandler(QObject):
    projectDataUpdate = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.project = Project()
        self.editorHandler = editorHandler(self.project)
        self.ProjectWindow = projectWindow()
        self.ActiveWindow = self.ProjectWindow
        self.connectSlots()
    
    def start(self):
        self.ProjectWindow.show()

    def fileBrowse(self):
        tempWindow = fileBrowser("spectra")
        tempWindow.fileOpened.connect(lambda x: self.addFile(x))
        tempWindow.openFile()
    
    def addFile(self, fname):
        self.ProjectWindow.addFile(fname)
        self.project.addSpecFile(fname)
        self.openFile(fname)

    def openFile(self, fname):
        self.editorHandler.openFile(fname)

    def connectSlots(self):
        self.ProjectWindow.fileAdded.connect(self.fileBrowse)
        self.editorHandler.projectDataUpdate.connect(lambda x: self.project.updateProject(x))
        
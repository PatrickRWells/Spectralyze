from remote import Remote
from plotHandler import plotHandler
from PyQt5.QtCore import pyqtSignal, QObject

class editorHandler(QObject):
    projectDataUpdate = pyqtSignal(dict)
    def __init__(self, project):
        super().__init__()
        self.project = project
        self.plotHandler = plotHandler(self.project)
        self.connectSlots()

    def openFile(self, fname):
        self.plotHandler.start(fname)
    
    def connectSlots(self):
        self.plotHandler.projectDataUpdate.connect(lambda x: self.projectDataUpdate.emit(x))
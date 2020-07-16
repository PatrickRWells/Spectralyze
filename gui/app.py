from select_data import dataSelectWindow
from startupWindow import startupWindow
from projectWindow import projectWindow
from PyQt5.QtWidgets import QApplication
from keckcode.deimos import deimosmask1d

import matplotlib.pyplot as plt
from remote import Remote
from plothandler import plotHandler

class spectraApp(QApplication):
    def __init__(self):
        super().__init__([])
        self.activeWindow = startupWindow()
        self.connectSignals()
        self.activeWindow.show()
        
    def connectSignals(self):
        self.activeWindow.newProject.connect(lambda: self.newProject())
    
    def handleFileOpen(self, fname):
        self.startupWindow.close()
        self.remote = Remote()
        self.plothandler = plotHandler(fname, self.remote)
        self.remote.show()

    def newProject(self):
        self.activeWindow.close()
        self.activeWindow = projectWindow()
        self.activeWindow.show()


from select_data import dataSelectWindow
from startupWindow import startupWindow
from projectWindow import projectWindow
from PyQt5.QtWidgets import QApplication
from keckcode.deimos import deimosmask1d

import matplotlib.pyplot as plt
from remote import Remote
from projectHandler import projectHandler

class spectraApp(QApplication):
    def __init__(self):
        super().__init__([])
        self.startupWindow = startupWindow()
        self.activeWindow = self.startupWindow
        self.connectSignals()
        self.activeWindow.show()
        
    def connectSignals(self):
        self.startupWindow.newProject.connect(lambda: self.newProject())

    def newProject(self):
        self.projectHandler = projectHandler()
        self.projectHandler.start()


from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog


class startupWindow(QWidget):
    newProject = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        
        self.newButton = newProjectButton()
        self.openButton = prevProjectButton()
        self.layout.addWidget(self.newButton)
        self.layout.addWidget(self.openButton)
        self.setLayout(self.layout)

        self.connectSlots()

    def openFileBrowser(self):
        self.fileBrowser.initFileBrowser()

    
    def connectSlots(self):
        self.newButton.clicked.connect(lambda: self.newProject.emit())

class newProjectButton(QPushButton):
    def __init__(self):
        super().__init__('New Project') 


class prevProjectButton(QPushButton):
    def __init__(self):
        super().__init__('Open Project')

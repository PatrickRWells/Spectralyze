from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QApplication, QLabel, QListWidget
from PyQt5.QtCore import pyqtSignal


class startupView(QWidget):
    addProject = pyqtSignal(str)
    openSavedProject =  pyqtSignal(str)
    removeSavedProject = pyqtSignal(str)
    def __init__(self, projectlist):
        super().__init__()
        self.projectList = projectlist
        self.layout = QVBoxLayout()
        self.newProjectButton = QPushButton("Add New Project")
        self.openProjectButton = QPushButton("Open Previous Project")
        self.layout.addWidget(self.newProjectButton)
        self.layout.addWidget(self.openProjectButton)
        self.setLayout(self.layout)
        self.connectSlots()
        self.newProjectWindow = None
        self.openProjectWindow = None
    
    def connectSlots(self):
        self.newProjectButton.clicked.connect(self.newProject)
        self.openProjectButton.clicked.connect(self.openProject)

        
    
    def newProject(self):
        if self.newProjectWindow is None:
            self.newProjectWindow = newProjectWindow()
            self.newProjectWindow.createProject.connect(lambda x: self.addProject.emit(x))
            self.hide()
            self.newProjectWindow.show()

    def openProject(self):
        if self.openProjectWindow is None:
            self.openProjectWindow = openProjectWindow(self.projectList)
            self.openProjectWindow.openProject.connect(lambda x: self.open(x))
            self.openProjectWindow.removeProject.connect(lambda x: self.removeSavedProject.emit(x))

        self.hide()
        self.openProjectWindow.show()

    def open(self, text):
        self.openSavedProject.emit(text)
    



class newProjectWindow(QWidget):
    createProject = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.label = QLabel("Project Name:")
        self.nameEdit = QLineEdit()
        self.createButton = QPushButton("Create...")
        self.topLayout.addWidget(self.label)
        self.topLayout.addWidget(self.nameEdit)
        self.layout.addLayout(self.topLayout)
        self.layout.addWidget(self.createButton)
        self.setLayout(self.layout)
        self.connectSignals()
    
    def connectSignals(self):
        self.createButton.clicked.connect(self.createPressed)
    
    def createPressed(self):
        title = self.nameEdit.text()
        self.createProject.emit(title)
        self.hide()

class openProjectWindow(QWidget):
    openProject = pyqtSignal(str)
    removeProject = pyqtSignal(str)
    def __init__(self, projectlist):
        super().__init__()
        self.layout = QVBoxLayout()
        self.list = QListWidget()
        self.list.addItems(projectlist)
        self.openButton = QPushButton("Open project")
        self.removeButton = QPushButton("Remove Selected Project")
        self.lower = QHBoxLayout()
        self.layout.addWidget(self.list)
        self.lower.addWidget(self.openButton)
        self.lower.addWidget(self.removeButton)
        self.layout.addLayout(self.lower)
        self.setLayout(self.layout)
        self.connectSignals()
    
    def setList(self, files):
        self.list.addItems(files)

    def connectSignals(self):
        self.openButton.clicked.connect(self.sendOpen)
        self.removeButton.clicked.connect(self.sendRemove)
    
    def sendOpen(self):
        name = self.list.currentItem()
        self.openProject.emit(name.text())
        self.hide()
    
    def sendRemove(self):
        name = self.list.currentItem()
        index = self.list.currentRow()
        self.list.takeItem(index)
        self.removeProject.emit(name.text())
        self.update()
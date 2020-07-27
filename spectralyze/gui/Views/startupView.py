from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QApplication, QLabel, QListWidget
from PyQt5.QtCore import pyqtSignal


class startupView(QWidget):
    addProject = pyqtSignal(str)
    openSavedProject =  pyqtSignal(str)
    removeSavedProject = pyqtSignal(str)
    def __init__(self, global_config, file_manager):
        super().__init__()
        self.global_config = global_config
        self.fileManager = file_manager
        self.projectList = self.fileManager.getSavedProjects()
        self.newProjectWindow = None
        self.setupWidgets()
        self.connectSlots()

    def setupWidgets(self):
        self.list = QListWidget()
        self.list.addItems(self.projectList)
        self.layout = QVBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.buttons = {'open': QPushButton("Open Project"), 
                        'remove': QPushButton("Remove Project"),
                        'new': QPushButton("New Project")}
        
        for name, button in self.buttons.items():
            self.bottomLayout.addWidget(button)

        self.layout.addWidget(self.list)
        self.layout.addLayout(self.bottomLayout)
        self.setLayout(self.layout)


    def connectSlots(self):
        self.buttons['open'].clicked.connect(self.openProject)
        self.buttons['remove'].clicked.connect(self.removeProject)
        self.buttons['new'].clicked.connect(self.newProject)   
    
    def newProject(self):
        if self.newProjectWindow is None:
            self.newProjectWindow = newProjectWindow()
            self.newProjectWindow.cancel.connect(self.show)
            self.newProjectWindow.createProject.connect(lambda x: self.addProject.emit(x))
        self.hide()
        self.newProjectWindow.show()

    def removeProject(self):
        name = self.list.currentItem()
        index = self.list.currentRow()
        self.list.takeItem(index)
        self.removeSavedProject.emit(name.text())
        self.update()


    def openProject(self):
        if self.list.count():
            selected = self.list.currentItem().text()
            self.openSavedProject.emit(selected)
    


class newProjectWindow(QWidget):
    createProject = pyqtSignal(str)
    cancel = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.label = QLabel("Project Name:")
        self.nameEdit = QLineEdit()
        self.createButton = QPushButton("Create...")
        self.cancelButton = QPushButton("Cancel")
        self.topLayout.addWidget(self.label)
        self.topLayout.addWidget(self.nameEdit)
        self.bottomLayout.addWidget(self.createButton)
        self.bottomLayout.addWidget(self.cancelButton)
        self.layout.addLayout(self.topLayout)
        self.layout.addLayout(self.bottomLayout)
        self.setLayout(self.layout)
        self.connectSignals()
    
    def connectSignals(self):
        self.createButton.clicked.connect(self.createPressed)
        self.cancelButton.clicked.connect(self.cancel.emit)
    
    def createPressed(self):
        title = self.nameEdit.text()
        self.createProject.emit(title)
        self.hide()
    def cancelPressed(self):
        self.hide()
        self.cancel.emit()
    

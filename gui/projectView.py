from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget, QToolButton, QLabel, QApplication, QStackedWidget, QSizePolicy
from PyQt5.QtCore import pyqtSignal
from fileBrowse import fileBrowser
from PyQt5.QtCore import pyqtSignal
from projectModel import projectModel
from spectraNavigatorView import spectraNavigatorView
from os.path import basename
import datetime


class projectView(QWidget):
    saveProject = pyqtSignal(str)
    def __init__(self, project):
        super().__init__()

        self.model = project
        self.fileBrowser = None
        self.spectraNavigatorViews = {}
        self.spectraNavigatorWidget = QStackedWidget()

        self.layout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()

        self.projectNameLabel = QLabel("Project: {}".format(self.model.name))
        self.saveButton = QPushButton("Save Project")
        self.saveLabel = QLabel("")

        self.fileList = fileList(self.model.getFileNames())

        self.leftLayout.addWidget(self.projectNameLabel)
        self.leftLayout.addWidget(self.fileList)
        self.leftLayout.addWidget(self.saveButton)
        self.leftLayout.addWidget(self.saveLabel)
        self.layout.addLayout(self.leftLayout)
        self.layout.addWidget(self.spectraNavigatorWidget)

        self.setLayout(self.layout)
        self.resize(100, 300)
        self.connectSignals()
        self.connectSlots()
        self.loadModel()
    
    def loadModel(self):
        files = self.model.getFileNames()
        if files:
            for file in files:
                self.spectraNavigatorViews.update({file: spectraNavigatorView(self.model.getSpectraModel(file))})
                self.spectraNavigatorWidget.addWidget(self.spectraNavigatorViews[file])
            self.spectraNavigatorWidget.setCurrentIndex(0)

    
    def connectSignals(self):
        pass

    def connectSlots(self):
        self.fileList.addFile.connect(self.getFile)
        self.fileList.removeFile.connect(lambda x: self.removeFile(x))
        self.fileList.currentFileChanged.connect(lambda x: self.setActiveFile(x))
        self.saveButton.clicked.connect(self.saveProjectClicked)

    def getFile(self):
        if self.fileBrowser is None:
            self.fileBrowser = fileBrowser("spectra")
            self.fileBrowser.fileOpened.connect(lambda x: self.addFile(x)) 
        
        self.fileBrowser.openFile()

    def addFile(self, fname):
        self.model.addFile(fname)
        self.spectraNavigatorViews.update({fname: spectraNavigatorView(self.model.getSpectraModel(fname))})
        self.spectraNavigatorWidget.addWidget(self.spectraNavigatorViews[fname])
        self.fileList.updateFileList(basename(fname))

    def removeFile(self, fname):
        pass

    def setActiveFile(self, name):
        index = 0
        for k, v in self.spectraNavigatorViews.items():
            if name in k:
                self.spectraNavigatorWidget.setCurrentIndex(index)
                if not self.spectraNavigatorWidget.isVisible():
                    self.spectraNavigatorWidget.show()
                break
            else:
                index += 1 

    def saveProjectClicked(self):
        time = datetime.datetime.now()
        self.saveLabel.setText("Project saved at {}".format(time.strftime("%H:%M")))
        if not self.saveLabel.isVisible():
            self.saveLabel.show()

        self.saveProject.emit(self.model.name)


class fileList(QWidget):
    
    addFile = pyqtSignal()
    removeFile = pyqtSignal(str)
    currentFileChanged = pyqtSignal(str)
    
    def __init__(self, files=None):
        super().__init__()
        self.list= QListWidget()
        if files is not None:
            for file in files:
                self.list.addItem(basename(file))
        self.layout = QVBoxLayout()
        self.setMinimumHeight(400)
        self.setMinimumWidth(100)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
        self.buttonLayout = QHBoxLayout()

        self.addButton = QPushButton()
        self.removeButton = QPushButton()
        self.addButton.setText('+')
        self.removeButton.setText('-')
        self.buttonLayout.addWidget(self.removeButton)
        self.buttonLayout.addWidget(self.addButton)
        self.fileLabel = QLabel("Files")

        self.layout.addWidget(self.fileLabel)
        self.layout.addWidget(self.list)
        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)
        self.connectSignals()
    
    def connectSignals(self):
        self.addButton.clicked.connect(lambda: self.addFile.emit())
        self.removeButton.clicked.connect(lambda x: self.removeFile.emit(x))
        self.list.itemSelectionChanged.connect(self.updateSelection)
    
    def updateFileList(self, file):
        self.list.addItem(file)
        self.update()
    
    def updateSelection(self):
        selection = self.list.currentItem()
        self.currentFileChanged.emit(selection.text())
    

if __name__ == "__main__":
    app = QApplication([])
    project = projectModel("Test")

    ProjectView = projectView(project)
    ProjectView.show()
    app.exec_()

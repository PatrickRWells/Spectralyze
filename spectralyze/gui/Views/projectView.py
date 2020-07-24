from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget, QToolButton, QLabel, QApplication, QStackedWidget, QSizePolicy
from PyQt5.QtCore import pyqtSignal
from fileBrowse import fileBrowser
from PyQt5.QtCore import pyqtSignal
from spectralyze.gui.Models.projectModel import projectModel
from spectraNavigatorView import spectraNavigatorView
import datetime
import os


class projectView(QWidget):
    CONFIG_FILE = os.path.join(os.environ['SPECTRALYZE_CONFIG'], "file_views.toml")
    saveProject = pyqtSignal(str)
    def __init__(self, project):
        super().__init__()

        self.model = project
        self.fileBrowser = None
        self.fileViews = {}

        self.setupWidgets()

        self.resize(100, 300)
        self.connectSignals()
        self.connectSlots()
    

    def setupWidgets(self):
        self.layout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.fileViewsWidget = self.model.getWidget()
        self.projectNameLabel = QLabel("Project: {}".format(self.model.name))
        self.saveButton = QPushButton("Save Project")
        self.saveLabel = QLabel("")
        self.fileList = fileList(self.model.getFileNames())
        self.leftLayout.addWidget(self.projectNameLabel)
        self.leftLayout.addWidget(self.fileList)
        self.leftLayout.addWidget(self.saveButton)
        self.leftLayout.addWidget(self.saveLabel)
        self.layout.addLayout(self.leftLayout)
        self.layout.addWidget(self.fileViewsWidget)
        self.setLayout(self.layout)


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
        self.fileList.updateFileList(os.path.basename(fname))

    def removeFile(self, fname):
        pass

    def setActiveFile(self, name):
        self.model.setActive(name)


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
                self.list.addItem(os.path.basename(file))
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
    fname1 = "/Volumes/Workspace/Data/reduced/Science/spec1d_d0721_0057-2209m1_DEIMOS_2017Jul21T091032.880.fits"
    fname2 = "/Volumes/Workspace/Data/reduced/Science/spec1d_d0721_0058-2209m1_DEIMOS_2017Jul21T094139.725.fits"
    app = QApplication([])
    project = projectModel("Test")
    project.addFile(fname1, 'keckcode_deimos1d')
    project.addFile(fname2, 'keckcode_deimos1d')

    ProjectView = projectView(project)
    ProjectView.show()
    app.exec_()

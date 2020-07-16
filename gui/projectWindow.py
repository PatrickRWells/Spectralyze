from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget, QToolButton, QLabel
from PyQt5.QtCore import pyqtSignal
from select_data import fileBrowser
from remote import Remote
from plothandler import plotHandler

class projectWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.fileController = fileListController()
        

        self.fileLabel = QLabel("Files")
        self.layout = QVBoxLayout()
        self.fileList = QListWidget()
        self.fileList.setMinimumHeight(200)
        self.fileList.setMinimumWidth(100)
        self.buttonLayout = QHBoxLayout()

        self.addButton = QPushButton()
        self.addButton.setText('+')

        self.buttonLayout.addWidget(self.addButton)

        self.layout.addWidget(self.fileLabel)
        self.layout.addWidget(self.fileList)
        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)
        self.resize(100, 300)
        self.connectSignals()
        self.connectSlots()

    def connectSignals(self):
        pass

    def connectSlots(self):
        self.addButton.pressed.connect(self.fileBrowse)

    def fileBrowse(self):
        tempWindow = fileBrowser("spectra")
        tempWindow.fileOpened.connect(lambda x: self.addFile(x))
        tempWindow.openFile()
    
    def addFile(self, fname):
        self.fileController.append(fname)
        self.fileList.addItem(fname)
        self.remote = Remote()
        self.plotHandler = plotHandler(fname, self.remote)
        self.remote.show()


class fileListController(list):
    def __init__(self):
        super().__init__()
    


from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget, QToolButton, QLabel
from PyQt5.QtCore import pyqtSignal
from select_data import fileBrowser
from remote import Remote
from plotHandler import plotHandler
from PyQt5.QtCore import pyqtSignal


class projectWindow(QWidget):
    fileAdded = pyqtSignal()
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
    
    def addFile(self, fname):
        self.fileList.addItem(fname)

    def connectSignals(self):
        pass

    def connectSlots(self):
        self.addButton.pressed.connect(lambda: self.fileAdded.emit())


class fileListController(list):
    def __init__(self):
        super().__init__()
    


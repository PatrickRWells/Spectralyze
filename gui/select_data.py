from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSignal

class dataSelectWindow(QWidget):
    fileOpened = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.fileBrowser = fileBrowser('spectra')

        self.layout = QVBoxLayout()
        
        self.open_button = openSpecButton()
        self.prev_button = openPrevButton()
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.prev_button)
        self.setLayout(self.layout)

        self.connectSlots()
        self.connectSignals()

    def openFileBrowser(self):
        self.fileBrowser.initFileBrowser()

    
    def connectSlots(self):
        self.open_button.clicked.connect(self.fileBrowser.openFile)
        
    def connectSignals(self):
        self.fileBrowser.fileOpened.connect(lambda x: self.openFile(x))

    def openFile(self, file):
        self.fileOpened.emit(file)

class fileBrowser(QWidget):
    types = {
        'general': "All Files (*)",
        'spectra': "Fits Files (*.fits)"
    }
    fileOpened = pyqtSignal(str)
    def __init__(self, type):
        super().__init__()

        assert type in self.types.keys(), "FBoxType not found"
        self.type = type

        self.title = "Browse"    
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
    
    def openFile(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNameDialog()

    def openFileNameDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", self.types[self.type])
        if fileName:
            self.fileOpened.emit(fileName)

class openSpecButton(QPushButton):
    def __init__(self):
        super().__init__('Open 1d Spectra') 


class openPrevButton(QPushButton):
    def __init__(self):
        super().__init__('Open Previous')

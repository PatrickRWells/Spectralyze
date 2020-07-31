from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class dataSelectWindow(QWidget):
    """
    A basic file browser
    There is a lot to be done here.
    """
    fileOpened = pyqtSignal(dict)
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
        self.fileBrowser.fileOpened.connect(lambda x: self.fileOpened.emit(x))

    def openFile(self, file):
        self.fileOpened.emit(file)

class fileBrowser(QWidget):
    types = {
        'general': "All Files (*)",
        'spectra': "Fits Files (*.fits)"
    }
    fileOpened = pyqtSignal(dict)
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
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "/Volumes/workspace/Data/reduced/Science", self.types[self.type])
        if fileName:
            if self.type == 'spectra':
                self.fileOpened.emit({fileName: 'keckcode_deimos1d'})
                #For now, this is the only type of file we have a configuration for

    

class fileTypeSelector(QWidget):
    def __init__(self):
        pass

class openSpecButton(QPushButton):
    def __init__(self):
        super().__init__('Open 1d Spectra') 


class openPrevButton(QPushButton):
    def __init__(self):
        super().__init__('Open Previous')

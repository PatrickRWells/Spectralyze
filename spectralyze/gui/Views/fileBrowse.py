from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
import toml
import os




class fileBrowser(QFileDialog):
    def __init__(self, global_config):
        self.global_config = global_config
        self.CONFIG_FILE = os.path.join(self.global_config['config_location'],
                                        self.global_config['fileBrowser'])
        self.config = toml.load(self.CONFIG_FILE)
        super().__init__()  


    def browseSaveLocation(self, ftype):
        if ftype in self.config['ftypes']:
            filter = self.config['ftypes'][ftype]['filter']
            fname = self.getSaveFileName(filter=filter)
            return fname

    def browseOpenLocation(self, ftype):
        if ftype in self.config['ftypes']:
            filter = self.config['ftypes'][ftype]['filter']
            fname = self.getOpenFileName(filter=filter)
            return fname

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


class fileTypeSelector(QWidget):
    def __init__(self):
        pass

class openSpecButton(QPushButton):
    def __init__(self):
        super().__init__('Open 1d Spectra') 


class openPrevButton(QPushButton):
    def __init__(self):
        super().__init__('Open Previous')

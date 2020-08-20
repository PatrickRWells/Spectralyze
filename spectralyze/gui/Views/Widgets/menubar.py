from PyQt5.QtWidgets import QMenuBar, QAction
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
import toml
import os 

class MenuBar(QMenuBar):
    exportMeta = pyqtSignal()
    importMeta = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setup()
    
    def setup(self):
        self.fileMenu = self.addMenu("File")
        self.ex = QAction(QIcon(''), 'Export File Data')
        self.im = QAction(QIcon(''), 'Import File Data')
        self.ex.triggered.connect(self.exportMeta.emit)
        self.im.triggered.connect(self.importMeta.emit)
        self.fileMenu.addAction(self.ex)
        self.fileMenu.addAction(self.im)



    def connectSignals(self):
        pass
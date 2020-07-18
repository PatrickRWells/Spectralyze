from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QCheckBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator, QDoubleValidator



class SpectrumNavigatorTool(QWidget):
        goNext = pyqtSignal()
        goPrev = pyqtSignal()

        def __init__(self):
            super().__init__()
            self.layout = QHBoxLayout()
            self.prevButton = QPushButton('Previous')
            self.nextButton = QPushButton('Next')
            self.layout.addWidget(self.prevButton)
            self.layout.addWidget(self.nextButton)
            self.connectSlots()
            self.setLayout(self.layout)

        def connectSlots(self):
            self.nextButton.clicked.connect(lambda: self.goNext.emit())
            self.prevButton.clicked.connect(lambda: self.goPrev.emit())
        
class SmoothingTool(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.smoothLabel = QLabel("Smoothing (px)")
        self.smoothBoxEdit = QLineEdit()
        self.intOnly = QIntValidator()
        self.smoothBoxEdit.setValidator(self.intOnly)
        self.smoothBoxEdit.setFixedWidth(30)
        self.smoothButton = QPushButton("OK")
        self.undoSmooth = QPushButton("Undo")
        self.layout.addWidget(self.smoothLabel)
        self.layout.addWidget(self.smoothBoxEdit)
        self.layout.addWidget(self.smoothButton)
        self.layout.addWidget(self.undoSmooth)
        self.setLayout(self.layout)
    
    def reset(self):
        self.smoothBoxEdit.setText('0')




class ZGuessTool(QWidget):
    def __init__(self):
        super().__init__()
        self.zGuessLabel = QLabel("Z Guess")
        self.zGuessBoxEdit = QLineEdit()
        self.zGuessEnforce = QDoubleValidator()
        self.zGuessBoxEdit.setValidator(self.zGuessEnforce)
        self.zGuessBoxEdit.setFixedWidth(50)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.zGuessLabel)
        self.layout.addWidget(self.zGuessBoxEdit)
        self.setLayout(self.layout)
    
    def setZ(self,z):
        self.zGuessBoxEdit.setText(str(z))

    def reset(self):
        self.zGuessBoxEdit.clear()

class SpectralLineTool(QWidget):
    linesUpdate = pyqtSignal(dict)
    def __init__(self):
        super().__init__()    
        self.layout = QHBoxLayout()
        self.checkLayout = QVBoxLayout()
        self.spectralLineLabel = QLabel("Spectral Lines")
        self.checkA = QCheckBox("Strong Emission")
        self.checkB = QCheckBox("All Emission")
        self.checkC = QCheckBox("Absorption")

        self.checkLayout.addWidget(self.checkA)
        self.checkLayout.addWidget(self.checkB)
        self.checkLayout.addWidget(self.checkC)
        self.layout.addWidget(self.spectralLineLabel)
        self.layout.addLayout(self.checkLayout)
        self.setLayout(self.layout)
        self.connectSlots()
    
    def connectSlots(self):
        self.checkA.stateChanged.connect(self.updateSpectra)
        self.checkB.stateChanged.connect(self.updateSpectra)
        self.checkC.stateChanged.connect(self.updateSpectra)
    
    def updateSpectra(self):
        spectra = {'strongem': self.checkA.isChecked(), 'em': self.checkB.isChecked(), 'abs': self.checkC.isChecked()}
        self.linesUpdate.emit(spectra)

    def reset(self):
        self.checkA.setChecked(False)
        self.checkB.setChecked(False)
        self.checkC.setChecked(False)   

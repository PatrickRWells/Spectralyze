from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import pyqtSignal


class Remote(QWidget):
    goNext = pyqtSignal()
    goPrev = pyqtSignal()
    goSmooth = pyqtSignal(int)
    goUndoSmooth = pyqtSignal()
    goZGuess = pyqtSignal(float)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.innerTop = QHBoxLayout()
        self.inner1 = QHBoxLayout()


        self.nextButton = goNextButton()
        self.prevButton = goPreviousButton()
        
        self.smoothLabel = QLabel("Smoothing (px)")
        self.smoothBoxEdit = QLineEdit()
        self.intOnly = QIntValidator()
        self.smoothBoxEdit.setValidator(self.intOnly)
        self.smoothBoxEdit.setFixedWidth(30)
        self.smoothButton = QPushButton("OK")
        self.undoSmooth = QPushButton("Undo")

        self.innerTop.addWidget(self.prevButton)
        self.innerTop.addWidget(self.nextButton)
        
        self.inner1.addWidget(self.smoothLabel)
        self.inner1.addWidget(self.smoothBoxEdit)
        self.inner1.addWidget(self.smoothButton)
        self.inner1.addWidget(self.undoSmooth)

        self.inner2 = QHBoxLayout()
        self.zGuessLabel = QLabel("Z Guess")
        self.zGuessBoxEdit = QLineEdit()
        self.zGuessEnforce = QDoubleValidator()
        self.zGuessBoxEdit.setValidator(self.zGuessEnforce)
        self.zGuessBoxEdit.setFixedWidth(30)

        self.inner2.addWidget(self.zGuessLabel)
        self.inner2.addWidget(self.zGuessBoxEdit)

        self.layout.addLayout(self.innerTop)
        self.layout.addLayout(self.inner1)
        self.layout.addLayout(self.inner2)

        self.setLayout(self.layout)
        self.connectSlots()
    
    def connectSlots(self):
        self.nextButton.clicked.connect(self.nextPressed)
        self.prevButton.clicked.connect(self.prevPressed)
        self.smoothButton.clicked.connect(self.smoothPressed)
        self.undoSmooth.clicked.connect(self.undoSmoothPressed)
        self.zGuessBoxEdit.textChanged.connect(self.zGuessChanged)

    def nextPressed(self):
        self.goNext.emit()
    def prevPressed(self):
        self.goPrev.emit()
    
    def smoothPressed(self):
        smoothing=int(self.smoothBoxEdit.text())
        self.goSmooth.emit(smoothing)

    def undoSmoothPressed(self):
        self.goUndoSmooth.emit()
        
    def zGuessChanged(self):
        if self.zGuessBoxEdit.text():
            zGuess = float(self.zGuessBoxEdit.text())
            self.goZGuess.emit(zGuess)

    def updateZ(self, zGuess):
        if zGuess != 0:
            self.zGuessBoxEdit.setText(str(zGuess))
        else:
            self.zGuessBoxEdit.setText(str(0))

class goNextButton(QPushButton):
    def __init__(self):
        super().__init__('Next') 


class goPreviousButton(QPushButton):
    def __init__(self):
        super().__init__('Previous')


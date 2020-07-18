from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSignal
import spectraNavigatorWidgets as widgets


class spectraToolboxView(QWidget):
    nextPressed = pyqtSignal()
    prevPressed = pyqtSignal()
    smoothPressed = pyqtSignal(int)
    undoSmoothPressed = pyqtSignal()
    zGuessInput = pyqtSignal(float)
    def __init__(self):
        super().__init__()
        self.spectrumNavigator = widgets.SpectrumNavigatorTool()
        self.smoothTool = widgets.SmoothingTool()
        self.zGuessTool = widgets.ZGuessTool()
        self.spectralLineTool = widgets.SpectralLineTool()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.spectrumNavigator)
        self.layout.addWidget(self.smoothTool)
        self.layout.addWidget(self.zGuessTool)
        self.layout.addWidget(self.spectralLineTool)
        self.setLayout(self.layout)
        self.connectSignals()
    
    def connectSignals(self):
        self.spectrumNavigator.nextButton.pressed.connect(lambda: self.nextPressed.emit())
        self.spectrumNavigator.prevButton.pressed.connect(lambda: self.prevPressed.emit())
        self.smoothTool.smoothButton.pressed.connect(self.smoothSpectra)
        self.smoothTool.undoSmooth.pressed.connect(lambda: self.undoSmoothPressed.emit())
        self.zGuessTool.zGuessBoxEdit.textChanged.connect(self.zGuessChanged)
    
    def smoothSpectra(self):
        smoothing = int(self.smoothTool.smoothBoxEdit.text())
        self.smoothPressed.emit(smoothing)
    
    def zGuessChanged(self):
        zGuess = self.zGuessTool.zGuessBoxEdit.text()
        if not zGuess:
            zGuess = "0"
        if zGuess[0] == '.':
            zGuess = '0' + zGuess
        self.zGuessInput.emit(float(zGuess))
        
    def setZ(self, z):
        self.zGuessTool.zGuessBoxEdit.setText(str(z))
        self.zGuessTool.zGuessBoxEdit.repaint()
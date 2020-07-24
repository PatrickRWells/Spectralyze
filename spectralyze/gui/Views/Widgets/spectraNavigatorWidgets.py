from PyQt5.QtWidgets  import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QCheckBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator, QDoubleValidator
import toml
import os
"""
    Widgets for use with a spectra view

"""



class SpectrumNavigatorTool(QWidget):
        """

        next/previous buttons

        """
        signal = pyqtSignal(str)

        def __init__(self):
            super().__init__()
            self.prevButton = QPushButton('Previous')
            self.nextButton = QPushButton('Next')

            self.layout = QHBoxLayout()

            self.layout.addWidget(self.prevButton)
            self.layout.addWidget(self.nextButton)
            
            self.setLayout(self.layout)
            self.connectSlots()

        def connectSlots(self):
            self.nextButton.clicked.connect(lambda: self.signal.emit("next"))
            self.prevButton.clicked.connect(lambda: self.signal.emit("previous"))
        
class SmoothingTool(QWidget):
    """
    Tool for inputing and apply smoothing
    """
    signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.smoothLabel = QLabel("Smoothing (px)")

        self.smoothBoxEdit = QLineEdit()
        self.intOnly = QIntValidator()
        self.smoothBoxEdit.setValidator(self.intOnly)
        self.smoothBoxEdit.setFixedWidth(30)

        self.smoothButton = QPushButton("OK")
        self.undoSmooth = QPushButton("Undo")
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.smoothLabel)
        self.layout.addWidget(self.smoothBoxEdit)
        self.layout.addWidget(self.smoothButton)
        self.layout.addWidget(self.undoSmooth)
        self.connectSignal()
        self.setLayout(self.layout)
    
    def reset(self):
        self.smoothBoxEdit.setText('0')
    
    def connectSignal(self):
        self.smoothButton.clicked.connect(self.updateSmoothing)
        self.undoSmooth.clicked.connect(lambda: self.updateSmoothing(True))

    def updateSmoothing(self, undo=False):
        if not self.smoothBoxEdit.text():
            pass
        else:
            if undo:
                self.reset()
                self.signal.emit(0)
            else:
                self.signal.emit(int(self.smoothBoxEdit.text()))




class ZGuessTool(QWidget):
    """
    Tool for inputting or display a redshift guess
    """
    signal = pyqtSignal(float)
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
        self.connectSignal()
        self.setLayout(self.layout)
    

    def setZ(self,z):
        self.zGuessBoxEdit.setText(str(z))

    def reset(self):
        self.zGuessBoxEdit.clear()
    
    def connectSignal(self):
        self.zGuessBoxEdit.textChanged.connect(self.updateGuess)
    
    def update(self, value):
        self.zGuessBoxEdit.setText(str(value))
        self.zGuessBoxEdit.repaint()

    def updateGuess(self):
        text = self.zGuessBoxEdit.text()
        if text:
            self.signal.emit(float(text))
        else:
            self.signal.emit(0)

class LineUpdateTool(QWidget):
    CONFIG_FILE = os.path.join(os.environ['SPECTRALYZE_CONFIG'], "spectral_lines.toml")
    """
    Checkbox widget for drawing spectral in a graph

    Constructor argument:
        name: Human readible title
        linetypes {id: line-name}
            id: id used for communication with other processes
            line-name: Human readable name of line

    """
    signal = pyqtSignal(dict)
    def __init__(self, config_type):
        super().__init__()    
        self.config_type = config_type
        self.config = toml.load(self.CONFIG_FILE)

        self.spectralLineLabel = QLabel(self.config[config_type]['name'])
        self.checkBoxWidgets = {}

        for id, line in self.config[config_type]["lines"].items():
            self.checkBoxWidgets.update({QCheckBox(line): id})

        self.checkLayout = QVBoxLayout()

        for widget in self.checkBoxWidgets.keys():
            self.checkLayout.addWidget(widget)

        self.layout = QHBoxLayout()

        self.layout.addWidget(self.spectralLineLabel)
        self.layout.addLayout(self.checkLayout)
        self.setLayout(self.layout)

        self.connectSlots()
    
    def connectSlots(self):
        for key in self.checkBoxWidgets.keys():
            key.stateChanged.connect(self.updateSpectra)
                
    def updateSpectra(self):
        spectra = {id: box.isChecked() for box, id in self.checkBoxWidgets.items()}
        self.signal.emit(spectra)

    def reset(self):
        for widget in self.checkBoxWidgets.keys():
            widget.setChecked(False)



if __name__ == "__main__":
    config = toml.load("config/spectral_lines.toml")
    app = QApplication([])
    window = LineUpdateTool("Spectral Lines", config['keckcode']['lines'])
    window.show()
    window.linesUpdate.connect(lambda x: print(x))

    app.exec_()

    print(config)
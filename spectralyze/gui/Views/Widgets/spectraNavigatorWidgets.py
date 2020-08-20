from PyQt5.QtWidgets  import (QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, 
                              QPushButton, QLineEdit, QLabel, QCheckBox, QComboBox, QSlider)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
import toml
import os
"""
    Widgets for use with a spectra view

"""



class SpectrumNavigatorTool(QWidget):
        """

        next/previous buttons, jump tool

        """
        signal = pyqtSignal(dict)

        def __init__(self):
            super().__init__()



            self.upperLayout = QHBoxLayout()
            self.lowerLayout = QHBoxLayout()
            self.layout = QVBoxLayout()
            self.setupWidgets()
            self.connectSlots()
        
        
        def setupWidgets(self):

            self.prevButton = QPushButton('Previous')
            self.nextButton = QPushButton('Next')
            self.jumpLabel = QLabel("jump To")
            self.jumpBox = QLineEdit()
            self.numberLabel = QLabel("out of {}")
            self.goButton = QPushButton("Go")
            self.jumpBox.setValidator(QIntValidator())
            self.jumpBox.setFixedWidth(30)



            self.lowerLayout.addWidget(self.prevButton)
            self.lowerLayout.addWidget(self.nextButton)
            self.upperLayout.addWidget(self.jumpLabel)
            self.upperLayout.addWidget(self.jumpBox)
            self.upperLayout.addWidget(self.numberLabel)
            self.upperLayout.addWidget(self.goButton)
            self.upperLayout.setContentsMargins(2, 2, 5, 5)

            self.layout.addLayout(self.upperLayout)
            self.layout.addLayout(self.lowerLayout)

            self.setLayout(self.layout)            


        def connectSlots(self):
            self.nextButton.clicked.connect(lambda: self.signal.emit({'increment': 'next'}))
            self.prevButton.clicked.connect(lambda: self.signal.emit({'increment': 'previous'}))
            self.goButton.clicked.connect(self.jump)
            self.jumpBox.returnPressed.connect(self.jump)
        
        def jump(self):
            num = int(self.jumpBox.text())
            if num < self.nspec:
                self.signal.emit({'jump': num-1})

        def update(self, data):
            for key, val in data.items():
                if key == 'nspec':
                    self.nspec = val
                    text = self.numberLabel.text()
                    self.numberLabel.setText(text.format(self.nspec))
            self.repaint()
        
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
        self.smoothBoxEdit.returnPressed.connect(self.updateSmoothing)

    def updateSmoothing(self, undo=False):
        if not self.smoothBoxEdit.text():
            pass
        else:
            if undo:
                self.reset()
                self.signal.emit(0)
            else:
                self.signal.emit(int(self.smoothBoxEdit.text()))



class spectraInfo(QWidget):
    signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.text = "Slit id: {}"
        self.label = QLabel('Hi')
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
    
    def update(self, data):
        for name, value in data.items():
            if name == 'slitid':
                self.label.setText(self.text.format(value))
        self.repaint()

class ZGuessTool(QWidget):
    """
    Tool for inputting or display a redshift guess
    """
    signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.zGuessLabel = QLabel("Z Guess")

        self.zGuessBoxEdit = QLineEdit()
        self.zGuessEnforce = QDoubleValidator()
        self.zGuessBoxEdit.setValidator(self.zGuessEnforce)
        self.zGuessBoxEdit.setFixedWidth(50)
        self.confidenceWidget = QComboBox()
        self.confidenceWidget.addItems(['', 'High', 'Medium', 'Low'])
        self.confidenceLabel = QLabel("Confidence")
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.zGuessLabel)
        self.layout.addWidget(self.zGuessBoxEdit)
        self.layout.addWidget(self.confidenceLabel)
        self.layout.addWidget(self.confidenceWidget)
        self.connectSignal()
        self.setLayout(self.layout)
    

    def setZ(self,z):
        self.zGuessBoxEdit.setText(str(z))

    def reset(self):
        self.zGuessBoxEdit.clear()
    
    def connectSignal(self):
        self.zGuessBoxEdit.textChanged.connect(self.updateGuess)
        self.confidenceWidget.currentTextChanged.connect(self.updateConfidence)
    
    def update(self, data):
        for name, value in data.items():
            if name == "zguess":
                self.zGuessBoxEdit.setText(str(value))
                self.zGuessBoxEdit.update()
            elif name == "confidence":
                if value:
                    self.confidenceWidget.setCurrentText(value)
                else:
                    self.confidenceWidget.setCurrentIndex(0)
        self.repaint()

    def updateGuess(self):
        text = self.zGuessBoxEdit.text()
        if text:
            self.signal.emit({'guess': float(text)})
        else:
            self.signal.emit({'guess': 0})
    
    def updateConfidence(self):
        text = self.confidenceWidget.currentText()
        self.signal.emit({'confidence': text})


class LineUpdateTool(QWidget):
    """
    Checkbox widget for drawing spectral in a graph

    Constructor argument:
        name: Human readible title
        linetypes {id: line-name}
            id: id used for communication with other processes
            line-name: Human readable name of line

    """
    signal = pyqtSignal(dict)
    def __init__(self, config_type, global_config):
        super().__init__()    
        self.global_config = global_config
        self.CONFIG_FILE = os.path.join(self.global_config['config_location'], 
                                        self.global_config['lineUpdateTool'])
        self.config_type = config_type
        self.config = toml.load(self.CONFIG_FILE)

        self.spectralLineLabel = QLabel(self.config[config_type]['name'])
        self.checkBoxWidgets = {}
        self.checkLayout = QVBoxLayout()

        for id, line in self.config[config_type]["lines"].items():
            widget = QCheckBox(line)
            self.checkBoxWidgets.update({id: widget})
            self.checkLayout.addWidget(widget)
        self.layout = QHBoxLayout()

        self.layout.addWidget(self.spectralLineLabel)
        self.layout.addLayout(self.checkLayout)
        self.setLayout(self.layout)

        self.connectSlots()
    
    def update(self, data):
        for key, value in data.items():
            self.checkBoxWidgets[key].setChecked(value)
        self.repaint()


    def connectSlots(self):
        for key, box in self.checkBoxWidgets.items():
            box.stateChanged.connect(self.updateSpectra)
                
    def updateSpectra(self):
        spectra = {id: box.isChecked() for id,box in self.checkBoxWidgets.items()}
        self.signal.emit(spectra)

    def reset(self):
        for widget in self.checkBoxWidgets.keys():
            widget.setChecked(False)


class classifierTool(QWidget):
    signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.classifier = QComboBox()
        self.classifier.addItems(['', 'Star', 'Galaxy', 'Unknown'])
        self.label = QLabel("Classification")
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.classifier)
        self.setLayout(self.layout)
        self.connectSlots()
    
    def connectSlots(self):
        self.classifier.currentTextChanged.connect(self.updateClasification)

    def updateClasification(self):
        text = self.classifier.currentText()
        self.signal.emit({'classification': text})

    def update(self, data):
        for name, value in data.items():
            if name == "classification":
                if value:
                    self.classifier.setCurrentText(value)
                else:
                    self.classifier.setCurrentIndex(0)
        self.repaint()

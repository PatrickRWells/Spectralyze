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
        signal = pyqtSignal(str)

        def __init__(self):
            super().__init__()
            self.prevButton = QPushButton('Previous')
            self.nextButton = QPushButton('Next')
            self.slider = QSlider(Qt.Horizontal)
            self.sliderLabel = QLabel("Jump To")

            self.upperLayout = QHBoxLayout()
            self.lowerLayout = QHBoxLayout()
            
            self.layout = QVBoxLayout()

            self.lowerLayout.addWidget(self.prevButton)
            self.lowerLayout.addWidget(self.nextButton)
            self.upperLayout.addWidget(self.sliderLabel)
            self.upperLayout.addWidget(self.slider)        
            self.layout.addLayout(self.upperLayout)
            self.layout.addLayout(self.lowerLayout)

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
                self.zGuessBoxEdit.repaint()
            elif name == "confidence":
                if value:
                    self.confidenceWidget.setCurrentText(value)
                else:
                    self.confidenceWidget.setCurrentIndex(0)
                self.confidenceWidget.repaint()

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

class modelTool(QWidget):
    """
    Tool for drawing a model spectra on top of the data.
    Currently this is very slow, so will not be included in main version
    """
    CONFIG_FILE = "/Users/patrick/code/spectra_code/dev/spectralyze/spectralyze/utils/config/spectra_model.toml"
    signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.config = toml.load(self.CONFIG_FILE)
        self.spectra = self.config['spectra'].keys()
        self.layout = QVBoxLayout()
        self.setupWidgets()
        self.connectSlots()
    
    def setupWidgets(self):
        self.label = QLabel("Model Spectra")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,1000)
        self.slider.setTracking(True)
        self.slider.setValue(250)
        self.comboBox = QComboBox()
        self.comboBox.addItem("none")
        for item in self.spectra:
            self.comboBox.addItem(item)
        self.lowerLayout = QHBoxLayout()
        self.label1 = QLabel("0.0")
        self.label2 = QLabel("2.0")
        self.label3 = QLabel("Redshift: {}".format(0.5))
        self.lowerLayout.addWidget(self.label1)
        self.lowerLayout.addWidget(self.slider)
        self.lowerLayout.addWidget(self.label2)
        self.lowestLayout = QHBoxLayout()

        self.button1 = QPushButton("<<<")
        self.button2 = QPushButton(">>>")
        self.lowestLayout.addWidget(self.button1)
        self.lowestLayout.addWidget(self.button2)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.label3)
        self.layout.addLayout(self.lowerLayout)
        self.layout.addLayout(self.lowestLayout)
        self.setLayout(self.layout)
    
    def connectSlots(self):
        self.button1.clicked.connect(self.decrease)
        self.button2.clicked.connect(self.increase)
        self.slider.valueChanged.connect(self.track)
        self.slider.sliderReleased.connect(self.update)
        self.comboBox.currentIndexChanged.connect(self.update)

    def increase(self):
        val = self.slider.value()
        if val < 1000:
            self.slider.setValue(val + 1)
            self.slider.repaint()
            self.update()
    def decrease(self):
        val = self.slider.value()
        if val > 0:
            self.slider.setValue(val-1)
            self.slider.repaint()
            self.update()

    def update(self):
        val = self.slider.value()
        self.label3.setText("Redshift: {}".format(round(val*0.002, 3)))
        self.label3.repaint()
        if self.comboBox.currentIndex() != 0:
            text = self.comboBox.currentText()
            self.signal.emit({'spectra': text, "z": val*0.002})


    def track(self):
        val = self.slider.value()
        self.label3.setText("Redshift: {}".format(round(val*0.002, 3)))
        self.label3.repaint()


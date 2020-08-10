from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, 
                            QFileDialog, QListWidget, QToolButton, QLabel, 
                            QApplication, QStackedWidget, QSizePolicy, QListWidgetItem, QTabWidget)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

from spectralyze.gui.Models.projectModel import projectModel
from spectralyze.gui.Views.fileBrowse import fileBrowser
import datetime
import os
import sys
import toml


class projectView(QWidget):
    """
    A Widget for displaying a project. Contains a list of files and a
    stacked widget that contains the individual file views
    
    attributes
    -------------
    model: Project model
    fileBrowser: File browser. Only instantiated if needed
    fileViews: Dictionary of individual file widgets
    
    """
    saveProject = pyqtSignal()
    def __init__(self, project, global_config):
        super().__init__()
        self.global_config = global_config
        self.CONFIG_FILE = os.path.join(self.global_config['config_location'], 
                                    self.global_config['projectView'])
        self.model = project
        self.fileBrowser = None
        self.fileViews = {}
        self.setupWidgets()
        self.connectSignals()
        self.connectSlots()


    def setupWidgets(self):
        """
        Basic layout includes an editable list of files
        And the stacked widget containing individual file views.
        """

        self.layout = QHBoxLayout()
        self.projectNavigator = ProjectNavigator(self.global_config)
        self.projectNavigator.update({'fileList': self.model.getFileNames()})
        self.leftLayout = QVBoxLayout()
        self.fileViewsWidget = self.model.getWidget()
        self.projectNameLabel = QLabel("Project: {}".format(self.model.name))
        self.saveButton = QPushButton("Save Project")
        self.saveLabel = QLabel("")
        self.leftLayout.addWidget(self.projectNameLabel)
        self.leftLayout.addWidget(self.projectNavigator)
        self.leftLayout.addWidget(self.saveButton)
        self.leftLayout.addWidget(self.saveLabel)
        self.layout.addLayout(self.leftLayout)
        self.layout.addWidget(self.fileViewsWidget)
        self.setLayout(self.layout)


    def connectSignals(self):
        self.projectNavigator.signal.connect(self.handleSignal)

    def connectSlots(self):
        #self.fileList.addFile.connect(self.getFile)
        #self.fileList.removeFile.connect(lambda x: self.removeFile(x))
        #self.fileList.currentFileChanged.connect(lambda x: self.setActiveFile(x))
        self.saveButton.clicked.connect(self.saveProjectClicked)

    def addFile(self, files):
        for fname, ftype in files.items():
            self.model.addFile(fname, ftype)

    def removeFile(self, fname):
        self.model.removeFile(fname)

    def updateSelection(self, name):
        self.model.setActive(name)


    def saveProjectClicked(self):
        time = datetime.datetime.now()
        self.saveLabel.setText("Project saved at {}".format(time.strftime("%H:%M")))
        if not self.saveLabel.isVisible():
            self.saveLabel.show()

        self.saveProject.emit()
    
    def handleSignal(self, data):
        for k,v in data.items():
            if hasattr(self, k):
                f = getattr(self, k)
                f(v)


class ProjectNavigator(QTabWidget):
    signal = pyqtSignal(dict)
    def __init__(self, global_config):
        super().__init__()
        self.global_config = global_config
        self.CONFIG_FILE = os.path.join(self.global_config['config_location'], 
                                    self.global_config['projectNavigator'])

        self.config = toml.load(self.CONFIG_FILE)
        self.icon_root = self.global_config['resource_location']
        self.layout = QVBoxLayout()
        self.setup()
        self.setLayout(self.layout)

    def setup(self):
        self.widgets = {}
        self.icons = {}
        for name, data in self.config['widgets'].items():
            widget_type = getattr(sys.modules[__name__], data['widget'])
            widget = widget_type()
            self.widgets.update({name: widget})
            self.icons.update({name: data['icons']})
            img_loc = os.path.join(self.icon_root, self.icons[name]['inactive'])
            self.addTab(self.widgets[name], QIcon(img_loc), data['name'])

        self.setTabPosition(QTabWidget.West)
        self.connectSignals()
    
    def connectSignals(self):
        for name, widget in self.widgets.items():
            if hasattr(widget, 'signal'):
                widget.signal.connect(lambda x, y=name: self.handleSignal(x, y))
    
    def update(self, data):
        for key, val in data.items():
            if key in self.widgets:
                self.widgets[key].update(val)
    
    def handleSignal(self, data, widget):
        for key, val in data.items():
            callback = self.config['widgets'][widget]['callbacks'][key]
            if hasattr(self, callback):
                f =  getattr(self, callback)
                f(data)
            self.signal.emit({key: val})

class fileList(QWidget):
    signal = pyqtSignal(dict)

    def __init__(self, files={}, global_config={}):
        super().__init__()
        self.global_config = global_config
        self.list= QListWidget()
        if files is not None:
            for file in files.keys():
                self.list.addItem(os.path.basename(file))
        self.layout = QVBoxLayout()
        self.setMinimumHeight(400)
        self.setMinimumWidth(100)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
        self.buttonLayout = QHBoxLayout()

        self.addButton = QPushButton()
        self.removeButton = QPushButton()
        self.addButton.setText('+')
        self.removeButton.setText('-')
        self.buttonLayout.addWidget(self.removeButton)
        self.buttonLayout.addWidget(self.addButton)
        self.fileBrowser = None
        self.layout.addWidget(self.list)
        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)
        self.connectSignals()
        

    def connectSignals(self):
        self.addButton.clicked.connect(self.getFile)
        self.removeButton.clicked.connect(self.fileRemoveClicked)
        self.list.itemSelectionChanged.connect(self.updateSelection)

    def update(self, files):
        for file in files:
            self.list.addItem(os.path.basename(file))
        super().update()

    def fileRemoveClicked(self):
        item = self.list.currentItem()
        row = self.list.currentRow()
        self.list.takeItem(row)
        super().update()
        self.signal.emit({'removeFile': item.text()})

    def updateSelection(self):
        selection = self.list.currentItem()
        self.signal.emit({'updateSelection': selection.text()})

    def addFile(self, data):
        for key, val in data.items():
            self.list.addItem(os.path.basename(key))
        super().update()
        self.signal.emit({'addFile': data})

    def getFile(self):
        if self.fileBrowser is None:
            self.fileBrowser = fileBrowser("spectra") #Currently this is the only type of file
                                                      #we know how to handle
            self.fileBrowser.fileOpened.connect(self.addFile)

        self.fileBrowser.openFile()



 


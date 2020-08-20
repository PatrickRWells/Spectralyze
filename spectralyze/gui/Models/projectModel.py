from PyQt5.QtWidgets import QStackedWidget, QFileDialog
from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSignal, QObject
from spectralyze.gui.Views.fileBrowse import fileBrowser
import time
threadPool = QThreadPool()

class projectModel(QObject):
    loadingComplete = pyqtSignal()
        self.loaded = {}


            att = v.attributes
            attributes.update({k: att})
        super().__init__()
        self.loaded = {}

            self.addFile(fname, configtype, attributes[fname])

    def setVersion(self, vnumber):
        self.version = vnumber
    def addFile(self, fname, config_type, attributes={}):
            loader = fileLoader(fname, config_type, self.global_config, attributes)
            loader.signals.result.connect(lambda x: self.updateFiles(x))
            threadPool.start(loader)

    def updateFiles(self, fileobj):
        self.fileModels.update({fileobj.fname: fileobj})
        self.loaded.update({fileobj.fname: True})
        if self.widget is not None:
            self.updateWidget()
        
        if len(self.loaded) == len(self.fileConfigs.keys()):
            self.loadingComplete.emit()

        return self.fileConfigs.keys()
    def getFileConfigs(self):
        return self.fileConfigs
        
        self.fileManager.saveProject(self)
    
    def exportData(self, fname, dtype):
        for key, val in self.fileModels.items():
            if fname in key:
                name = QFileDialog.getSaveFileName()
                val.exportFileData(name[0])
    
    def importData(self, fname, data, dtype):
        for key, val in self.fileModels.items():
            if fname in key:
                browser = fileBrowser("spectra meta") #Currently this is the only type of file
                browser.fileOpened.connect(lambda x: val.importFileData(x))
                browser.openFile()
    

class fileLoader(QRunnable):
    def __init__(self, file, config_type, global_config, attributes = {}):
        super().__init__()
        self.file = file
        self.config_type = config_type
        self.global_config = global_config
        self.signals = signals()
        self.attributes = attributes

    def run(self):
        data = getFileModel(self.file, 'spectra', self.config_type, self.global_config)
        if self.attributes:
            data.updateAttributes(self.attributes)
        
        self.signals.result.emit(data)

class signals(QObject):
    result=pyqtSignal(object)
    def __init__(self):
        super().__init__()


class projectLoader(QObject):
    loadingComplete = pyqtSignal(object)
    def __init__(self, fname, fileManager):
        super().__init__()
        self.fname = fname
        self.fileManager = fileManager
        self.signals = signals()
    
    def loadProject(self):
        with open(self.fname, 'rb') as f:
            project = pickle.load(f)
            project.setFileManager(self.fileManager)
            project.loadingComplete.connect(lambda x=project: self.loadingComplete.emit(x))

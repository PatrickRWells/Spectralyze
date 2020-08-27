class fileModel:
    def __init__(self):
        self.fileManager = None
    def __getstate__(self):
        pass

    def __setstate__(self, state):
        pass

    def updateAttributes(self, attributes):
        pass
    
    def setFileManager(self, f):
        self.fileManager = f

def getFileModel(fname, type, config_type, global_config):
    if type == 'spectra':
        from spectralyze.gui.Models.spectraModelWrappers import getSpectraModel
        return getSpectraModel(fname, config_type, global_config)
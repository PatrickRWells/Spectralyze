from spectraModel import spectraModel
import pickle
import os

class projectModel:
    def __init__(self, name):
        super().__init__()
        self.spectraModels = {}
        self.saveLocation = ""
        self.name = name

    def addFile(self, fname):
        if fname in self.spectraModels.keys():
            pass
        else:
            self.spectraModels.update({fname: spectraModel(fname)})

    def getFileNames(self):
        return self.spectraModels.keys()
    
    def getSpectraModel(self, fname):
        return self.spectraModels[fname]

    def saveProjectModel(self, fname):
        self.saveLocation = fname
        pickle.dump(self, self.saveLocation)

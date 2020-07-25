from pathlib import Path
import os
import pickle
import toml
from spectralyze.gui.Models.projectModel import projectModel

class fileManager:
    PROJECT_SAVE_LOCATION = os.path.join(str(Path.home()), '.spectralyze')
    PROJECT_CONFIG_LOCATION = os.path.join(PROJECT_SAVE_LOCATION, 'projects.toml')
    def __init__(self):
        pass

    def saveProject(self, model):
        self.checkSaveDir()
        self.checkSaveConfig()
        filename = os.path.join(self.PROJECT_SAVE_LOCATION, '.'.join([model.name, 'spec']))
        self.checkPreviousSave(model.name, filename)
        with open(filename, 'wb') as projectfile:
            pickle.dump(model, projectfile)

    def checkSaveDir(self):
        if not os.path.exists(self.PROJECT_SAVE_LOCATION):
            os.mkdir(self.PROJECT_SAVE_LOCATION)
    
    def checkSaveConfig(self):
        if not os.path.exists(self.PROJECT_CONFIG_LOCATION):
            file = open(self.PROJECT_CONFIG_LOCATION, 'w')
            file.close()
    
    def checkPreviousSave(self, name, fname):
        fileConfig = toml.load(self.PROJECT_CONFIG_LOCATION)
        fileConfig.update({name: fname})
        with open(self.PROJECT_CONFIG_LOCATION, 'w') as file:
            toml.dump(fileConfig, file)




if __name__ == "__main__":
    fileManager = fileManager()

    fname = "/Volumes/workspace/data/reduced/Science/spec1d_d0721_0057-2209m1_DEIMOS_2017Jul21T091032.880.fits"
    fname2 = "/Volumes/workspace/Data/reduced/Science/spec1d_d0721_0058-2209m1_DEIMOS_2017Jul21T094139.725.fits"


    model = projectModel("test2")
    model.addFile(fname, 'keckcode_deimos1d')
    model.addFile(fname2, 'keckcode_deimos1d')
    
    fileManager.saveProject(model)

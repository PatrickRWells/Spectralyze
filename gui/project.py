from astropy.io import fits


class Project:
    def __init__(self):
        self.specMetas = {}

    
    def addSpecFile(self, fname):
        assert type(fname) == str, "Unable to open"
        hdu = fits.open(fname)
        hdr0 = hdu[0].header
        nspec = hdr0['nspec']
        tempMeta = {fname: specMeta(nspec)}
        self.specMetas.update(tempMeta)


    def addZGuess(self, fname, num, zGuess):
        self.specMetas[fname].addZ(num, zGuess)
    
    def getZGuess(self, fname, num):
        return self.specMetas[fname].z[num]
    
    def updateProject(self, data):
        for k,v in data.items():
            if k == 'zGuess':
                self.addZGuess

class specMeta:
    def __init__(self, numSpecs):
        self.numSpecs = numSpecs
        self.z = [0] * numSpecs
    
    def addZ(self, num, z):
        self.z[num] = z
    
    def returnZ(self, num):
        return self.z[num]


class Project:
    def __init__(self):
        self.specMetas = {}

    
    def addSpecFile(self, fname, numSpec):
        assert type(fname) == str, "Unable to open"
        tempMeta = {fname: specMeta(numSpec) }
        self.specMetas.update(tempMeta)

    def addZGuess(self, fname, num, zGuess):
        self.specMetas[fname].addZ(num, zGuess)
    
    def getZGuess(self, fname, num):
        return self.specMetas[fname].z[num]

class specMeta:
    def __init__(self, numSpecs):
        self.numSpecs = numSpecs
        self.z = [0] * numSpecs
    
    def addZ(self, num, z):
        self.z[num] = z
        print("GOT IT")
    
    def returnZ(self, num):
        return self.z[num]
from spectraModel import spectraModel



class spectraNavigatorModel:
    def __init__(self, fname):
        self.fname = fname
        self.SpectraModel = spectraModel(fname)
        self.nspec = self.SpectraModel.numspec
        self.currSpec = 0
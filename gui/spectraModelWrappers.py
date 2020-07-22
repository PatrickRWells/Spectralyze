from keckcode.deimos import deimosmask1d
from spectraModel import abstractSpectraModel


class deimos1DSpectra(abstractSpectraModel):
    def __init__(self, fname):
        super().__init__(self, "deimos1d")
        self.mask = deimosmask1d.DeimosMask1d(self.fname)
        self.plot = self.mask.plot(0)
        self.nspec = self.mask.nspec
        self.curspec = 0

    def nextGraph(self, **kwargs):
        if self.curspec < self.nspect - 1:
            self.curspec += 1
            self.plot.clf()
            self.mask.plot(self.curspec, fig=self.plot)
            

    def prevGraph(self, **kwargs):
        pass

    def smoothGraph(self, **kwargs):
        pass
    
    def zGuessUpdate(self, **kwargs):
        pass

    def linesUpdate(self, **kwargs):
        pass

    


    
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['mask']
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.mask = deimosmask1d.DeimosMask1d(self.fname)



def getSpectraModel(self, configtype, file):
    if configtype == "deimos1d":
        return deimos1DSpectra(file)

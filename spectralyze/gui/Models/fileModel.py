class fileModel:
    pass


def getFileModel(fname, type, config_type):
    if type == 'spectra':
        from spectralyze.gui.Models.spectraModelWrappers import getSpectraModel
        return getSpectraModel(fname, config_type)
class fileModel:
    def __init__(self):
        pass
    def __getstate__(self):
        pass

    def __setstate__(self, state):
        print(state)


def getFileModel(fname, type, config_type, global_config):
    if type == 'spectra':
        from spectralyze.gui.Models.spectraModelWrappers import getSpectraModel
        return getSpectraModel(fname, config_type, global_config)
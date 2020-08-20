import time

CURRENT_VERSION = '0.0.2'

def updateProjectVersion(project):
    print("UPDATING MODEL")
    for fileModel in project.fileModels.values():
        for specname in fileModel.keys:
            fileModel.attributes.update({specname: {}})

   
        if 'zguess' in fileModel.attributes.keys():
            for index, val in enumerate(fileModel.keys):
                fileModel.attributes[val].update({'zguess': fileModel.attributes['zguess'][index]})
            fileModel.attributes.pop('zguess')
        if 'confidence' in fileModel.attributes.keys():
            for index, val in enumerate(fileModel.keys):
                fileModel.attributes[val].update({'confidence': fileModel.attributes['confidence'][index]})
            fileModel.attributes.pop('confidence')
        if 'classification' in fileModel.attributes.keys():
            for index, val in enumerate(fileModel.keys):
                fileModel.attributes[val].update({'classification': fileModel.attributes['classification'][index]})
            fileModel.attributes.pop('classification')

    project.setVersion(CURRENT_VERSION)


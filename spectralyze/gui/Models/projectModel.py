    """
    Model for storing and retrieving project data.
    attributes
    ----------
    fileManager: File manager for saving data to disk
    fileModels: Individual file models. Type will depend on kind of file
    fileWidgets: References to the UI widgets associated with the files
    fileConfigs: Dictionary containing file types    
    """
        """
        Used when loading a previously saved project
        """
        """
        Prepare project data for disk storage.
        References to UI, and other things that are stateless are removed
        """
        """
        Reads in the data as outputted by __getstate___
        Automatically called when the project is opened
        """
            self.fileModels[fname].updateAttributes(attributes[fname])
        """
        Adds a file to the project. 
        fname: absolute path to the file
        config_type: one of the config types from 
        """
        """
        Removes a file from the project
        """
        """
        Gets a UI widget for a project.
        Presently, this is just a stack of the widgets associated
        with the various files
        """

        """
        Updates the widget. If no name is passed, checks
        for new file models and adds their widget if found.
        If a name is passed, removes that widget from the stack
        """
        """
        Sets the active widget (i.e. top of the stack)
        """
        """
        Get UI widget for a particular file. 
        """
        """
        Sends itself to the file manager to be saved
        """
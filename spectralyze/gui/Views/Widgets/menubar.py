from PyQt5.QtWidgets import QMenuBar, QAction
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
import toml
import os 

class MenuBar(QMenuBar):
    signal = pyqtSignal(dict)
    def __init__(self, global_config):
        self.global_config = global_config
        self.CONFIG_FILE = os.path.join(self.global_config['config_location'], 
                                    self.global_config['menuBar'])
        self.config = toml.load(self.CONFIG_FILE)

        super().__init__()
        self.setup()
    
    def setup(self):
        self.menus = {}
        self.menuItems = {}
        for menu in self.config['menus']:
            menuData = self.config['menus'][menu]
            menuName = menuData['name']
            menuObj = self.addMenu(menuName)
            self.menus.update({menuName: menuObj})
            self.menuItems.update({menuName: {}})
            for action in menuData['actions']:
                actionData = menuData['actions'][action]
                actName = actionData['name']
                actTarget = actionData['target']
                icon = actionData['icon']
                if icon == 'None':
                    actObj = QAction(QIcon(''), actName)
                    actObj.triggered.connect(lambda x, y=action, z=actTarget: self.signal.emit({'target': z, 'action': y}))
                    actObj.isIconVisibleInMenu = False
                    menuObj.addAction(actObj)
                    self.menuItems[menuName].update({action:  actObj})

    

    def connectSignals(self):
        pass
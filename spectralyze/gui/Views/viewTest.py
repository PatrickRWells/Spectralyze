from projectView import projectView
from spectralyze.gui.Models.projectModel import projectModel
from PyQt5.QtWidgets import QApplication


fname = "/Volumes/workspace/data/reduced/Science/spec1d_d0721_0057-2209m1_DEIMOS_2017Jul21T091032.880.fits"
fname2 = "/Volumes/workspace/Data/reduced/Science/spec1d_d0721_0058-2209m1_DEIMOS_2017Jul21T094139.725.fits"

app = QApplication([])

model = projectModel("test")
model.addFile(fname, 'keckcode_deimos1d')
model.addFile(fname2, 'keckcode_deimos1d')
view = projectView(model)

view.show()
app.exec_()

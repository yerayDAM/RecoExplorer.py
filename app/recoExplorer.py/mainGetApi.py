from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QMessageBox

import os

class myMainWindow(object):
    def __init__(self, app):
        self.app = app # call init of QMainWindow, or QWidget or whatever)

        # se añade la intefaz que se desee
        self.ui = uic.loadUi('recoExplorer.py/view/GUI_Apikeyvirustotal.UI')
        self.ui.pushButton.clicked.connect(self.guardarApi)

        # se muestra la interfaz
        self.ui.show()
        self.run()

    def run(self):
        self.app.exec_()

#/////////////////////////////////////////////
#                                          ///
# START FUNCIONES AÑADIDAS                 ///
#                                          ///
#/////////////////////////////////////////////
    def cerrar_aplicacion(self):
        QtCore.QCoreApplication.quit()  # Cerrar la aplicación

    def guardarApi(self):
        api_key = self.ui.lineEdit.text()
        if not api_key:
            return

        # Guardar la API key en un archivo
        file_path = "recoExplorer.py/apikey-virustotal.txt"
        with open(file_path, "w") as f:
            f.write(api_key)
            self.cerrar_aplicacion()

#/////////////////////////////////////////////
#                                          ///
# END FUNCIONES AÑADIDAS                   ///
#                                          ///
#/////////////////////////////////////////////

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myMainWindow(app)

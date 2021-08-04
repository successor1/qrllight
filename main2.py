from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from views.test import Ui_Wizard
import sys

class Test(QtWidgets.QWizard, Ui_Wizard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.setupUi(self)

        myLineEdit= QLineEdit()
        self.wizardPage1.registerField("name",myLineEdit)
        self.registerField("name", self.nome1)
        self.label_2.setText(f'My name is : {self.field("name")}')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Test()
    mainWindow.show()
    sys.exit(app.exec_())

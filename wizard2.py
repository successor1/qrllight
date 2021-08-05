import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from main import QrlWallet

class MyWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(MyWizard, self).__init__(parent)

        self.introPage = IntroPage()
        self.firstPageOptionA = FirstPageOptionA()
        self.lastPage = LastPage()
        self.setPage(0, self.introPage)
        self.setPage(1, self.firstPageOptionA)
        self.setPage(2, self.lastPage)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self._doSomething)

    def _doSomething(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Yep, its connected.")
        msgBox.exec()

class IntroPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        
        self.setTitle("Welcome to QRL Light Wallet!")

        self.label_description = QLabel("Select option:")
        self.radiobutton_1 = QRadioButton("Create new wallet")
        self.radiobutton_2 = QRadioButton("Open wallet file")
        self.radiobutton_3 = QRadioButton("Restore wallet from seed")

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_description)
        layout.addWidget(self.radiobutton_1)
        layout.addWidget(self.radiobutton_2)
        layout.addWidget(self.radiobutton_3)

    def _nextPage(self):
        if self.radiobutton_1.isChecked():
            self.nextId()

class FirstPageOptionA(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(FirstPageOptionA, self).__init__(parent)

        self.NameLabel = QLabel("&Name:")
        self.NameLineEdit = QLineEdit()
        self.NameLabel.setBuddy(self.NameLineEdit)

        layout = QHBoxLayout(self)
        layout.addWidget(self.NameLabel)
        layout.addWidget(self.NameLineEdit)

class SecondPageOptionB(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(SecondPageOptionB, self).__init__(parent)

class ThirdPageOptionC(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ThirdPageOptionC, self).__init__(parent)

class LastPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(LastPage, self).__init__(parent)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MyWizard()
    mainWindow = QrlWallet()
    main.hide()
    main.setWindowModality(QtCore.Qt.ApplicationModal)
    main.show()
    mainWindow.show()
    sys.exit(app.exec_())
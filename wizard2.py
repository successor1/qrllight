import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from main import QrlWallet

class MyWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)


        self.introPage = IntroPage()
        self.firstPageOptionA = FirstPageOptionA()
        self.lastPage = LastPage()
        self.addPage(self.introPage)
        self.addPage(self.firstPageOptionA)
        self.addPage(self.lastPage)
        # self.setPage(0, self.introPage)
        # self.setPage(1, self.firstPageOptionA)
        # self.setPage(2, self.lastPage)

        self.button(QWizard.NextButton).clicked.connect(self._nextPage)
    def _nextPage(self):
        if self.currentPage() == self.introPage:
            if self.introPage == self.introPage.radiobutton_1.isChecked():
                return self.currentId() + 2
        # if self.introPage.radiobutton_1.isChecked():
        #     return self.currentId + 2



class IntroPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        
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

class FirstPageOptionA(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)


        self.NameLabel = QLabel("&Name:")
        self.NameLineEdit = QLineEdit()
        self.NameLabel.setBuddy(self.NameLineEdit)

        layout = QHBoxLayout(self)
        layout.addWidget(self.NameLabel)
        layout.addWidget(self.NameLineEdit)

class SecondPageOptionB(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)


class ThirdPageOptionC(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)


class LastPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.NameLabel = QLabel("&ummm:")
        self.NameLineEdit = QLineEdit()
        self.NameLabel.setBuddy(self.NameLineEdit)

        layout = QHBoxLayout(self)
        layout.addWidget(self.NameLabel)
        layout.addWidget(self.NameLineEdit)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MyWizard()
    mainWindow = QrlWallet()
    main.hide()
    main.setWindowModality(QtCore.Qt.ApplicationModal)
    main.show()
    mainWindow.show()
    sys.exit(app.exec_())
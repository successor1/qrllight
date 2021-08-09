import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from main import QrlWallet
import subprocess
from models.model import Model

class MyWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.introPage = IntroPage()
        self.firstPageOptionA = FirstPageOptionA(self)
        self.SecondPageOptionA = SecondPageOptionA()
        self.secondPageOptionB = SecondPageOptionB()
        self.thirdPageOptionC = ThirdPageOptionC()
        self.lastPage = LastPage()
        self.addPage(self.introPage)
        self.addPage(self.firstPageOptionA)
        self.addPage(self.SecondPageOptionA)
        self.addPage(self.secondPageOptionB)
        self.addPage(self.thirdPageOptionC)
        self.addPage(self.lastPage)


        self.currentIdChanged.connect(self.next_callback)


    def next_callback(self, page_id: int):
        if page_id == 2 and self.last_page_id == 1:
            print(Model.getAddress())
        self.last_page_id = page_id


class IntroPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setTitle("Welcome to QRL Light Wallet!")

        self.label_description = QLabel("Select option:")
        self.radiobutton_1 = QRadioButton("Create new wallet")
        self.radiobutton_2 = QRadioButton("Open wallet file")
        self.radiobutton_3 = QRadioButton("Restore wallet from seed")
        self.radiobutton_2.setChecked(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_description)
        layout.addWidget(self.radiobutton_1)
        layout.addWidget(self.radiobutton_2)
        layout.addWidget(self.radiobutton_3)

    def nextId(self) -> int:
        if self.radiobutton_1.isChecked():
            return 1
        if self.radiobutton_2.isChecked():
            return 3
        if self.radiobutton_3.isChecked():
            return 4

        return 0

class FirstPageOptionA(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Create wallet!")

        self.name_label = QLabel("Name:")
        self.nameline_edit = QLineEdit()
        self.password_label = QLabel("Password (optional):")
        self.passwordline_edit = QLineEdit()
        self.directory_label = QLabel("Directory:")
        self.directoryline_edit = QLineEdit()

        layout = QVBoxLayout(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.nameline_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.passwordline_edit)
        layout.addWidget(self.directory_label)
        layout.addWidget(self.directoryline_edit)

    def nextId(self) -> int:
        return 2

class SecondPageOptionA(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Wallet seed")


class SecondPageOptionB(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Open wallet file")

        # self.openFileBtn = QtWidgets.QPushButton("Import wallet key file")
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.openFileBtn)
        # self.setLayout(layout)
        # self.openFileBtn.clicked.connect(self.openFileNameDialog)

        self.model = QFileSystemModel()
        self.model.setRootPath(r'C:\Users\31622\Documents')
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(r'C:\Users\31622\Documents'))
        
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setWindowTitle("Dir View")
        self.tree.resize(640, 480)
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        self.setLayout(windowLayout)

    @QtCore.pyqtSlot()
    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        # if user selected a file store its path to a variable
        if fileName:
            self.wizard().variable = fileName

class ThirdPageOptionC(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Restore your wallet")

        self.seed_label = QLabel("Enter your seed:")
        self.seedline_edit = QLineEdit()

        layout = QHBoxLayout(self)
        layout.addWidget(self.seed_label)
        layout.addWidget(self.seedline_edit)


class LastPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.NameLabel = QLabel("last page:")
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
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from main import QrlWallet
import subprocess
from models.model import Model
from models.aes import AESModel
from pyqrllib.pyqrllib import str2bin, XmssFast, mnemonic2bin, hstr2bin, bin2hstr, SHAKE_128, SHAKE_256, SHA2_256, getRandomSeed
import json


class MyWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(550, 400)
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
        self.SecondPageOptionA.save_wallet_file.clicked.connect(self.saveFile)
        self.secondPageOptionB.openFileBtn.clicked.connect(self.openFile)



    def next_callback(self, page_id: int):
        if page_id == 2 and self.last_page_id == 1:
            combo_height_short = self.firstPageOptionA.combo_height
            combo_hash_short = self.firstPageOptionA.combo_hash
            if combo_height_short.currentIndexChanged or combo_hash_short.currentIndexChanged:
                combo_height_options = {0: 8, 1: 10, 2: 12, 3: 14, 4: 16, 5: 18}
                combo_hash_options = {0: SHAKE_128, 1: SHAKE_256, 2: SHA2_256}
            qaddress, mnemonic, hexseed = Model.getAddress(combo_height_options[combo_height_short.currentIndex()], combo_hash_options[combo_hash_short.currentIndex()])
            self.SecondPageOptionA.qaddress.setText(qaddress)
            self.SecondPageOptionA.mnemonic.setText(mnemonic + "\n" + "\n")
            self.SecondPageOptionA.hexseed.setText(hexseed)
            # balance = Model.getAddressBalance(qaddress)
            # mainWindow.balance_label.setText(str(balance))
        self.last_page_id = page_id
    
    def saveFile(self):
        file_filter = 'Json file (*.json)'
        dialog_save_file_name = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save file',
            directory= 'wallet.json',
            filter=file_filter,
            initialFilter='Json file (*.json)')
        dialog = open(dialog_save_file_name[0], "w")
        dialog.write(json.dumps(AESModel.encrypt(self.SecondPageOptionA.qaddress.toPlainText() + " " + self.SecondPageOptionA.mnemonic.text().rstrip() + " " + self.SecondPageOptionA.hexseed.text(), self.firstPageOptionA.passwordline_edit.text())))
        dialog.close()

    def openFile(self):
        file_filter = 'Json file (*.json)'
        dialog_save_file_name = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            directory= '.json',
            filter=file_filter,
            initialFilter='Json file (*.json)')
        dialog = open(dialog_save_file_name[0], "w")
        dialog.write(json.dumps(AESModel.encrypt(self.SecondPageOptionA.qaddress.toPlainText() + " " + self.SecondPageOptionA.mnemonic.text().rstrip() + " " + self.SecondPageOptionA.hexseed.text(), self.firstPageOptionA.passwordline_edit.text())))
        dialog.close()

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

        self.setTitle("Create wallet")

        self.password_label = QLabel("Password (optional):")
        self.passwordline_edit = QLineEdit(self)
        self.passwordline_edit.setEchoMode(2)
        self.passwordline_edit.setPlaceholderText("Enter password")

        self.combo_height = QComboBox(self)
        self.combo_height.addItem("Tree height: 8 | Signatures: 256")
        self.combo_height.addItem("Tree height: 10 | Signatures: 1,024")
        self.combo_height.addItem("Tree height: 12 | Signatures: 4,096")
        self.combo_height.addItem("Tree height: 14 | Signatures: 16,384")
        self.combo_height.addItem("Tree height: 16 | Signatures: 65,536")
        self.combo_height.addItem("Tree height: 18 | Signatures: 262,144")

        self.combo_hash = QComboBox(self)
        self.combo_hash.addItem("Hash function: SHAKE_128")
        self.combo_hash.addItem("Hash function: SHAKE_256")
        self.combo_hash.addItem("Hash function: SHA2_256") 

        layout = QVBoxLayout(self)
        layout.addWidget(self.password_label)
        layout.addWidget(self.passwordline_edit)
        layout.addWidget(self.combo_height)
        layout.addWidget(self.combo_hash)

    def nextId(self) -> int:
        return 2

class SecondPageOptionA(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Wallet details")

        self.qaddress_description = QLabel("QRL Public address:")
        self.qaddress = QTextEdit()
        self.qaddress.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.mnemonic_description = QLabel("Mnemonic phrase:")
        self.mnemonic = QLabel()
        self.hexseed_description = QLabel("Hexseed:")
        self.hexseed = QLabel()

        self.save_wallet_file = QPushButton('Save secure wallet file')


        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.frame = QFrame(self)
        self.qaddress.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.qaddress.setFrameShadow(QFrame.Plain)
        self.qaddress.setLineWidth(1)

        self.mnemonic.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.mnemonic.setFrameShadow(QFrame.Plain)
        self.mnemonic.setLineWidth(1)
        self.mnemonic.setWordWrap(True)

        self.hexseed.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.hexseed.setFrameShadow(QFrame.Plain)
        self.hexseed.setLineWidth(1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.qaddress_description)
        layout.addWidget(self.qaddress)
        layout.addWidget(self.mnemonic_description)
        layout.addWidget(self.mnemonic)
        layout.addWidget(self.hexseed_description)
        layout.addWidget(self.hexseed)
        layout.addWidget(self.save_wallet_file)

    def nextId(self) -> int:
        return 5

class SecondPageOptionB(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Open wallet file")

        self.password_qlabel = QLabel("Password (optional):")
        self.passwordline_edit = QLineEdit()
        self.passwordline_edit.setEchoMode(2)
        self.passwordline_edit.setPlaceholderText("Enter password")
        self.openFileBtn = QPushButton("Import secure wallet file")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.password_qlabel)
        layout.addWidget(self.passwordline_edit)
        layout.addWidget(self.openFileBtn)
        self.setLayout(layout)

    # @QtCore.pyqtSlot()
    # def openFileNameDialog(self):
    #     options = QtWidgets.QFileDialog.Options()
    #     options |= QtWidgets.QFileDialog.DontUseNativeDialog
    #     fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
    #         self, "QFileDialog.getOpenFileName()", "",
    #         "All Files (*);;Python Files (*.py)", options=options)
    #     # if user selected a file store its path to a variable
    #     if fileName:
    #         self.wizard().variable = fileName

    def nextId(self) -> int:
        return 5

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
        self.setTitle("Success!")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MyWizard()
    mainWindow = QrlWallet()  
    main.hide()
    main.setWindowModality(QtCore.Qt.ApplicationModal)
    main.show()
    mainWindow.show()
    sys.exit(app.exec_())
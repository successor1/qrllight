from views.view_ui import Ui_mainWindow
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from views.view_ui import Ui_mainWindow
from views.about_window import Ui_Form
import sys
from models.model import Model
import models.TransferTransaction
from models.aes import AESModel
from pyqrllib.pyqrllib import str2bin, XmssFast, mnemonic2bin, hstr2bin, bin2hstr, SHAKE_128, SHAKE_256, SHA2_256, getRandomSeed
from qrl.core.misc import logger
from qrl.crypto.xmss import XMSS
from qrl.crypto.xmss import XMSS, hash_functions
from qrl.core.Wallet import Wallet, WalletDecryptionError
import qrcode
from PIL import Image
import re

import os
from binascii import hexlify, a2b_base64
from collections import namedtuple
from decimal import Decimal
from typing import List

import grpc
import simplejson as json
from google.protobuf.json_format import MessageToJson
from pyqrllib.pyqrllib import mnemonic2bin, hstr2bin, bin2hstr

from qrl.core import config
from qrl.core.Wallet import Wallet, WalletDecryptionError
from qrl.core.misc.helper import parse_hexblob, parse_qaddress
from qrl.core.MultiSigAddressState import MultiSigAddressState
from qrl.core.txs.MessageTransaction import MessageTransaction
from qrl.core.txs.SlaveTransaction import SlaveTransaction
from qrl.core.txs.TokenTransaction import TokenTransaction
from qrl.core.txs.Transaction import Transaction
from qrl.core.txs.TransferTokenTransaction import TransferTokenTransaction
from qrl.core.txs.TransferTransaction import TransferTransaction
from qrl.core.txs.multisig.MultiSigCreate import MultiSigCreate
from qrl.core.txs.multisig.MultiSigSpend import MultiSigSpend
from qrl.crypto.xmss import XMSS, hash_functions
from qrl.generated import qrl_pb2_grpc, qrl_pb2

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
        self.finished.connect(self.onFinished)



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
        data = []
        if QWizard.hasVisitedPage(self, 5):
            print(data)
        else:
            file_filter = 'Json file (*.json)'
            dialog_save_file_name = QFileDialog.getOpenFileName(
                parent=self,
                caption='Open file',
                directory= '.json',
                filter=file_filter,
                initialFilter='Json file (*.json)')
            dialog = open(dialog_save_file_name[0], "r")
            data.append(bytes.decode(AESModel.decrypt(json.load(dialog), self.secondPageOptionB.passwordline_edit.text())))
            dialog.close()

    def onFinished(self):
        qrl_address = []
        mnemonic = []
        hexseed = []
        if QWizard.hasVisitedPage(self, 2):
            qrl_address.append(self.SecondPageOptionA.qaddress.toPlainText())
            mnemonic.append(self.SecondPageOptionA.mnemonic.text().rstrip())
            hexseed.append(self.SecondPageOptionA.hexseed.text())
        elif QWizard.hasVisitedPage(self, 3):
            print(main.openFile)
            qrl_address.append(self.openFile[0])
        elif QWizard.hasVisitedPage(self, 4):
            if self.thirdPageOptionC.seedline_edit.text()[:6] ==  "absorb":
                qrl_address.append(Model.recoverAddressMnemonic(self.thirdPageOptionC.seedline_edit.text()))
                mnemonic.append(self.thirdPageOptionC.seedline_edit.text())
            elif self.thirdPageOptionC.seedline_edit.text()[:2] ==  "01":
                qrl_address.append(Model.recoverAddressHexseed(self.thirdPageOptionC.seedline_edit.text()))
                hexseed.append(self.thirdPageOptionC.seedline_edit.text())
        mainWindow.public_label_description.setText(qrl_address[0])
        mainWindow.public_label_description.setTextInteractionFlags(Qt.TextSelectableByMouse)
        img = qrcode.make(qrl_address[0])
        img_saved = img.save("views/images/qr_code.png")
        mainWindow.pixmap = QPixmap('views/images/qr_code.png')
        mainWindow.qr_image_label.setPixmap(mainWindow.pixmap)
        mainWindow.qr_image_label.setScaledContents(True)
        mainWindow.balance_label.setText("Balance: " + str(float(Model.getAddressBalance(qrl_address[0])) / 1000000000) + " QUANTA")


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

class QrlWallet(QtWidgets.QMainWindow, Ui_mainWindow, Ui_Form, QtWidgets.QWizard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.model = Model()

        self.send_button.clicked.connect(self.button_clicked)
        self.actionAbout.triggered.connect(self.about_popup)
        self.actionOfficial_website.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://theqrl.org")))
        self.actionQRL_whitepaper.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://docs.theqrl.org/")))
        self.actionQRL_whitepaper.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://raw.githubusercontent.com/theQRL/Whitepaper/master/QRL_whitepaper.pdf")))

    def button_clicked(self):
        qrl_address = []
        mnemonic = []
        hexseed = []
        if QWizard.hasVisitedPage(main, 2):
            qrl_address.append(main.SecondPageOptionA.qaddress.toPlainText())
            mnemonic.append(main.SecondPageOptionA.mnemonic.text().rstrip())
            hexseed.append(main.SecondPageOptionA.hexseed.text())
        elif QWizard.hasVisitedPage(main, 3):
            print(main.openFile())
        elif QWizard.hasVisitedPage(main, 4):
            if self.thirdPageOptionC.seedline_edit.text()[:6] ==  "absorb":
                qrl_address.append(Model.recoverAddressMnemonic(self.thirdPageOptionC.seedline_edit.text()))
                mnemonic.append(self.thirdPageOptionC.seedline_edit.text())
            elif self.thirdPageOptionC.seedline_edit.text()[:2] ==  "01":
                qrl_address.append(Model.recoverAddressHexseed(self.thirdPageOptionC.seedline_edit.text()))
                hexseed.append(self.thirdPageOptionC.seedline_edit.text())
        addrs_to = [bytes(hstr2bin(self.send_input.text()[1:]))]
        amounts = [(int(self.amount_input.text()) * 1000000000)]
        fee = str(float(self.fee_input.text()) * 1000000000)[:-2]
        xmss_pk = XMSS.from_extended_seed(hstr2bin(hexseed[0])).pk
        src_xmss = XMSS.from_extended_seed(hstr2bin(hexseed[0]))
        models.TransferTransaction.tx_transfer(
            addrs_to,
             amounts,
              fee,
              xmss_pk,
              src_xmss)
        QMessageBox.about(self, "Succesful transaction", "Sent!")
        balance_numbers_only = re.sub("[^0-9]", "", self.balance_label.text())
        update_label = float(float(int(balance_numbers_only) / 1000000000) - float(float(amounts[0])  / 1000000000.0) + (float(fee) / 1000000000.0))
        self.balance_label.setText("Balance: " + str(update_label) + " QUANTA")
        self.balance_label.adjustSize()

    def update(self):
        self.balance_label.adjustSize()

    def about_popup(self):
        self.dialog=QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.dialog)
        self.dialog.show() 


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MyWizard()
    mainWindow = QrlWallet()  
    main.hide()
    main.setWindowModality(QtCore.Qt.ApplicationModal)
    mainWindow.show()
    main.show()
    sys.exit(app.exec_())

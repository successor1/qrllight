from os import remove

from google.protobuf import message
from models import Slaves
from time import time
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
from views.about_ui import Ui_Form
from views.donate_ui import Ui_Form2
import sys
from models.model import Model
import models.TransferTransaction
from models.aes import AESModel
from pyqrllib.pyqrllib import hstr2bin, SHAKE_128, SHAKE_256, SHA2_256
from qrl.crypto.xmss import XMSS
from qrl.crypto.xmss import XMSS
import qrcode
from PIL import Image
import simplejson as json
from pyqrllib.pyqrllib import hstr2bin, XmssFast, QRLDescriptor
from qrl.crypto.xmss import XMSS
from qrl.crypto.doctest_data import *
import random
from models.GetMiniTransactionsByAddress import TableOutput
from datetime import datetime

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

class MyWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(550, 400)
        self.introPage = IntroPage()
        self.createWallet = CreateWallet()
        self.walletDetails = WalletDetails()
        self.createSeedByMouse = CreateSeedByMouse()
        self.walletDetailsExperimental = WalletDetailsExperimental()
        self.slavesJsonOptions = SlaveJsonOptions()
        self.createSlavesJson = CreateSlavesJson()
        self.openWalletFileSlaves = OpenWalletFileSlaves()
        self.openWalletFile = OpenWalletFile()
        self.restoreWallet = RestoreWallet()
        self.restoreWalletSlaves = RestoreWalletSlaves()
        self.lastPage = LastPage()
        self.addPage(self.introPage)
        self.addPage(self.createWallet)
        self.addPage(self.walletDetails)
        self.addPage(self.createSeedByMouse)
        self.addPage(self.walletDetailsExperimental)
        self.addPage(self.openWalletFile)
        self.addPage(self.restoreWallet)
        self.addPage(self.slavesJsonOptions)
        self.addPage(self.createSlavesJson)
        self.addPage(self.openWalletFileSlaves)
        self.addPage(self.restoreWalletSlaves)
        self.addPage(self.lastPage)

        self.currentIdChanged.connect(self.next_callback)
        self.walletDetails.save_wallet_file.clicked.connect(self.saveFile)
        self.walletDetailsExperimental.save_wallet_file.clicked.connect(self.saveFileExperimental)
        self.openWalletFile.openFileBtn.clicked.connect(self.openFile)
        self.openWalletFileSlaves.openFileBtn.clicked.connect(self.openFileSlaves)
        self.finished.connect(self.onFinished)

    seed_data = []
    data = []

    def next_callback(self, page_id: int):
        if page_id == 2 and self.last_page_id == 1:
            combo_height_short = self.createWallet.combo_height
            combo_hash_short = self.createWallet.combo_hash
            if combo_height_short.currentIndexChanged or combo_hash_short.currentIndexChanged:
                combo_height_options = {0: 8, 1: 10, 2: 12, 3: 14, 4: 16, 5: 18}
                combo_hash_options = {0: SHAKE_128, 1: SHAKE_256, 2: SHA2_256}
            qaddress, mnemonic, hexseed = Model.getAddress(combo_height_options[combo_height_short.currentIndex()], combo_hash_options[combo_hash_short.currentIndex()])
            self.walletDetails.qaddress.setText(qaddress)
            self.walletDetails.mnemonic.setText(mnemonic + "\n" + "\n")
            self.walletDetails.hexseed.setText(hexseed)
        if page_id == 4 and self.last_page_id == 3:
            combo_height_short = self.createSeedByMouse.combo_height
            combo_hash_short = self.createSeedByMouse.combo_hash
            if combo_height_short.currentIndexChanged or combo_hash_short.currentIndexChanged:
                combo_height_options = {0: 8, 1: 10, 2: 12, 3: 14, 4: 16, 5: 18}
                combo_hash_options = {0: SHAKE_128, 1: SHAKE_256, 2: SHA2_256}
            seed_data = [i for i in self.seed_data if int(i) < 255]
            random.shuffle(seed_data)
            new_seed_data = [int(g) for g in seed_data[:48]]
            qaddress, mnemonic, hexseed = Model.getAddressExperimental(combo_height_options[combo_height_short.currentIndex()], combo_hash_options[combo_hash_short.currentIndex()], tuple(new_seed_data[:48]))
            self.walletDetailsExperimental.qaddress.setText(qaddress)
            self.walletDetailsExperimental.mnemonic.setText(mnemonic + "\n" + "\n")
            self.walletDetailsExperimental.hexseed.setText(hexseed)
        if page_id == 8 and self.last_page_id == 9:
            qrl_address = []
            mnemonic = []
            hexseed = []
            qrl_address.append(main.data[0].split(" ")[0])
            mnemonic.append(" ".join(main.data[0].split(" ")[1:-1]))
            hexseed.append(main.data[0].split(" ")[35])
            xmss_pk = XMSS.from_extended_seed(hstr2bin(hexseed[0])).pk
            src_xmss = XMSS.from_extended_seed(hstr2bin(hexseed[0]))
            xmss_height = src_xmss.height
            xmss = XMSS.from_height(xmss_height)
            xmss_extended_seed = xmss.extended_seed
            Slaves.slave_tx_generate(xmss_pk, src_xmss, xmss_extended_seed)
        if page_id == 8 and self.last_page_id == 10:
            qrl_address = []
            mnemonic = []
            hexseed = []
            if QWizard.hasVisitedPage(main, 7):
                if main.restoreWalletSlaves.seedline_edit.text()[:6] ==  "absorb":
                    qrl_address.append(Model.recoverAddressMnemonic(main.restoreWalletSlaves.seedline_edit.text()))
                    mnemonic.append(main.restoreWalletSlaves.seedline_edit.text())
                    hexseed.append(Model.recoverHexseedMnemonic(main.restoreWalletSlaves.seedline_edit.text()))
                elif main.restoreWalletSlaves.seedline_edit.text()[:2] ==  "01":
                    qrl_address.append(Model.recoverAddressHexseed(main.restoreWalletSlaves.seedline_edit.text()))
                    mnemonic.append(Model.recoverMnemonicHexseed(main.restoreWalletSlaves.seedline_edit.text()))
                    hexseed.append(main.restoreWalletSlaves.seedline_edit.text())
            xmss_pk = XMSS.from_extended_seed(hstr2bin(hexseed[0])).pk
            src_xmss = XMSS.from_extended_seed(hstr2bin(hexseed[0]))
            xmss_height = src_xmss.height
            xmss = XMSS.from_height(xmss_height)
            xmss_extended_seed = xmss.extended_seed
            Slaves.slave_tx_generate(xmss_pk, src_xmss, xmss_extended_seed)
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
        dialog.write(json.dumps(AESModel.encrypt(self.walletDetails.qaddress.toPlainText() + " " + self.walletDetails.mnemonic.text().rstrip() + " " + self.walletDetails.hexseed.text(), self.createWallet.passwordline_edit.text())))
        dialog.close()

    def saveFileExperimental(self):
        file_filter = 'Json file (*.json)'
        dialog_save_file_name = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save file',
            directory= 'wallet.json',
            filter=file_filter,
            initialFilter='Json file (*.json)')
        dialog = open(dialog_save_file_name[0], "w")
        dialog.write(json.dumps(AESModel.encrypt(self.walletDetailsExperimental.qaddress.toPlainText() + " " + self.walletDetailsExperimental.mnemonic.text().rstrip() + " " + self.walletDetailsExperimental.hexseed.text(), self.createSeedByMouse.passwordline_edit.text())))
        dialog.close()


    def openFile(self) -> int:
        file_filter = 'Json file (*.json)'
        dialog_save_file_name = QFileDialog.getOpenFileName(
                parent=self,
                caption='Open file',
                directory= '.json',
                filter=file_filter,
                initialFilter='Json file (*.json)')
        try:
            dialog = open(dialog_save_file_name[0], "r")
            main.data.append(bytes.decode(AESModel.decrypt(json.load(dialog), self.openWalletFile.passwordline_edit.text())))
            dialog.close()
            QMessageBox.about(self, "Success!", "Correct password!")
        except ValueError:
            QMessageBox.warning(self, "Wrong password!", "You have entered the wrong password!")

    def openFileSlaves(self) -> int:
        file_filter = 'Json file (*.json)'
        dialog_save_file_name = QFileDialog.getOpenFileName(
                parent=self,
                caption='Open file',
                directory= '.json',
                filter=file_filter,
                initialFilter='Json file (*.json)')
        try:
            dialog = open(dialog_save_file_name[0], "r")
            main.data.append(bytes.decode(AESModel.decrypt(json.load(dialog), self.openWalletFileSlaves.passwordline_edit.text())))
            dialog.close()
            QMessageBox.about(self, "Success!", "Correct password!")
        except ValueError:
            QMessageBox.warning(self, "Wrong password!", "You have entered the wrong password!")


    def onFinished(self):
        qrl_address = []
        mnemonic = []
        hexseed = []
        if QWizard.hasVisitedPage(main, 2):
            qrl_address.append(main.walletDetails.qaddress.toPlainText())
            mnemonic.append(main.walletDetails.mnemonic.text().rstrip())
            hexseed.append(main.walletDetails.hexseed.text())
        elif QWizard.hasVisitedPage(main, 5):
            qrl_address.append(main.data[0].split(" ")[0])
            mnemonic.append(" ".join(main.data[0].split(" ")[1:-1]))
            hexseed.append(main.data[0].split(" ")[35])
        elif QWizard.hasVisitedPage(main, 6):
            if main.restoreWallet.seedline_edit.text()[:6] ==  "absorb":
                qrl_address.append(Model.recoverAddressMnemonic(main.restoreWallet.seedline_edit.text()))
                mnemonic.append(main.restoreWallet.seedline_edit.text())
                hexseed.append(Model.recoverHexseedMnemonic(main.restoreWallet.seedline_edit.text()))
            elif main.restoreWallet.seedline_edit.text()[:2] ==  "01":
                qrl_address.append(Model.recoverAddressHexseed(main.restoreWallet.seedline_edit.text()))
                mnemonic.append(Model.recoverMnemonicHexseed(main.restoreWallet.seedline_edit.text()))
                hexseed.append(main.restoreWallet.seedline_edit.text())
        elif QWizard.hasVisitedPage(main, 3):
            qrl_address.append(main.walletDetailsExperimental.qaddress.toPlainText())
            mnemonic.append(main.walletDetailsExperimental.mnemonic.text().rstrip())
            hexseed.append(main.walletDetailsExperimental.hexseed.text())
        mainWindow.public_label_description.setText(qrl_address[0])
        mainWindow.public_label_description.setTextInteractionFlags(Qt.TextSelectableByMouse)
        img = qrcode.make(qrl_address[0])
        img_saved = img.save("qr_code.png")
        mainWindow.pixmap = QPixmap('qr_code.png')
        mainWindow.qr_image_label.setPixmap(mainWindow.pixmap)
        mainWindow.qr_image_label.setScaledContents(True)
        mainWindow.ots_key_index_input.setText(str(int(Model.getAddressOtsKeyIndex(qrl_address[0]))))
        mainWindow.balance_label.setText("Balance: " + str(float(Model.getAddressBalance(qrl_address[0])) / 1000000000) + " QUANTA")
        recoveryWindow.mnemonic_label_text.setText(mnemonic[0])
        recoveryWindow.hexseed_label_text.setText(hexseed[0])
        rowPosition = mainWindow.transaction_table.rowCount()
        transaction_hashes = []
        transaction_hashes.append(TableOutput.getMiniTransactionsByAddressHashes(qrl_address[0]))
        timestamp_seconds = []
        amount = []
        amount_send_receive = []
        message_tx = []
        date_time = []
        for x in transaction_hashes[0]:
            resp = Model.getTransactionByHash(x)
            try:
                timestamp_seconds.append(resp["transaction"]["header"]["timestamp_seconds"])
                amount.append(resp["transaction"]["explorer"]["totalTransferred"])
            except KeyError:
                try:
                    amount.append((float(resp["transaction"]["tx"]["transfer"]["amounts"][0]) / 1000000000))
                except KeyError:
                    if resp["transaction"]["tx"]["transactionType"] == 'transfer_token':
                        amount.append("token transfer")
                    else:
                        amount.append("message")
            try:
                message_tx.append(resp["transaction"]["tx"]["message"]["message_hash"])
            except KeyError:
                message_tx.append(" ")
            try:
                amount_send_receive.append(resp["transaction"]["explorer"]["from_hex"])
            except KeyError:
                amount_send_receive.append(None)
        for i in timestamp_seconds:
            date_time.append(datetime.fromtimestamp(int(i)).strftime("%Y-%m-%d %I:%M:%S"))
        x = 0
        y = 1
        z = 2
        print(amount_send_receive)
        for _ in range(len(date_time)):
            mainWindow.transaction_table.insertRow(rowPosition)
        for date_box, description_box, amount_box, plusminus in zip(date_time, message_tx, amount, amount_send_receive):
            mainWindow.transaction_table.setItem(x, 0, QTableWidgetItem(date_box))
            mainWindow.transaction_table.setItem(0, y, QTableWidgetItem(str(description_box)))
            if plusminus == qrl_address[0]:
                mainWindow.transaction_table.setItem(0, z, QTableWidgetItem("-" + str(amount_box)))
            elif plusminus != qrl_address[0]:
                mainWindow.transaction_table.setItem(0, z, QTableWidgetItem("+" + str(amount_box)))
            x += 1
            y += 3
            z += 3

        # for x, y, x1, y2, plusminus, range_message, message in zip(range(len(date_time)), date_time, range(2, 30, 3), amount, amount_send_receive, range(1, 28, 3), message_tx):
        #     mainWindow.transaction_table.setItem(x , 0, QTableWidgetItem(y))
        #     mainWindow.transaction_table.setItem(0 , range_message, QTableWidgetItem(str(message)))
        #     if plusminus == None:
        #         mainWindow.transaction_table.setItem(0 , x1, QTableWidgetItem(str(y2)))
        #     elif plusminus != qrl_address[0]:
        #         mainWindow.transaction_table.setItem(0 , x1, QTableWidgetItem("+" + str(y2)))
        #     elif plusminus == qrl_address[0]:
        #         mainWindow.transaction_table.setItem(0 , x1, QTableWidgetItem("-" + str(y2)))

class IntroPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setTitle("Welcome to Qrllight Wallet v1.4!")

        self.label_description = QLabel("Select option:")
        self.radiobutton_1 = QRadioButton("Create new wallet")
        self.radiobutton_2 = QRadioButton("Open wallet file")
        self.radiobutton_3 = QRadioButton("Restore wallet from seed")
        self.Separador = QFrame()
        self.Separador.Shape(QFrame.HLine)
        self.Separador.setLineWidth(1)
        self.Separador.setFrameShape(QFrame.HLine)

        self.radiobutton_4 = QRadioButton("Create a Slaves.json")
        self.radiobutton_5 = QRadioButton("Create wallet by random mouse movements [Experimental] [Not safe]")
        self.radiobutton_2.setChecked(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_description)
        layout.addWidget(self.radiobutton_1)
        layout.addWidget(self.radiobutton_2)
        layout.addWidget(self.radiobutton_3)
        layout.addWidget(self.Separador)
        layout.addWidget(self.radiobutton_4)
        layout.addWidget(self.radiobutton_5)
        

    def nextId(self) -> int:
        if self.radiobutton_1.isChecked():
            return 1
        if self.radiobutton_2.isChecked():
            return 5
        if self.radiobutton_3.isChecked():
            return 6
        if self.radiobutton_4.isChecked():
            return 7
        if self.radiobutton_5.isChecked():
            return 3

        return 0

class CreateWallet(QtWidgets.QWizardPage):
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

class WalletDetails(QtWidgets.QWizardPage):
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
        return 11

class CreateSeedByMouse(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Generate entropy by mouse!")

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

        self.video_label = QtWidgets.QLabel()
        self.video_label.setStyleSheet("background-color: white; border: 1px solid black")
        self.video_label.setFixedWidth(510)
        self.video_label.setFixedHeight(175)

        tracker = MouseTracker(self.video_label)
        tracker.positionChanged.connect(self.on_positionChanged)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.password_label)
        layout.addWidget(self.passwordline_edit)
        layout.addWidget(self.combo_height)
        layout.addWidget(self.combo_hash)
        layout.addWidget(self.video_label)

        self.label_position = QtWidgets.QLabel(
            self.video_label, alignment=QtCore.Qt.AlignCenter
        )
        self.label_position.setStyleSheet('background-color: white; border: 1px solid black')

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_positionChanged(self, pos):
        delta = QtCore.QPoint(30, -15)
        self.label_position.show()
        self.label_position.move(pos + delta)
        self.label_position.setText("(%d, %d)" % (pos.x(), pos.y()))
        self.label_position.adjustSize()
        main.seed_data.append("%d" % (pos.x()))
        main.seed_data.append("%d" % (pos.y()))
        print(main.seed_data)


    def nextId(self) -> int:
        return 4

class MouseTracker(QtCore.QObject):
    positionChanged = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, widget):
        super().__init__(widget)
        self._widget = widget
        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, o, e):
        if o is self.widget and e.type() == QtCore.QEvent.MouseMove:
            self.positionChanged.emit(e.pos())
        return super().eventFilter(o, e)

class WalletDetailsExperimental(QtWidgets.QWizardPage):
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
        return 11

class SlaveJsonOptions(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Slaves.json requires a wallet")


        self.label_description = QLabel("Select option:")
        self.radiobutton_1 = QRadioButton("Open wallet file")
        self.radiobutton_2 = QRadioButton("Restore wallet from seed")

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_description)
        layout.addWidget(self.radiobutton_1)
        layout.addWidget(self.radiobutton_2)

    def nextId(self) -> int:
        if self.radiobutton_1.isChecked():
            return 9
        if self.radiobutton_2.isChecked():
            return 10
        return 0

class CreateSlavesJson(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.setTitle("Slaves.json is finished!")

        self.generatedslave_label = QLabel("Move slaves.json file from current directory to the mining node inside ~/.qrl/\n\nYou can close the wallet now.")
        self.slave_number_label = QLabel()

        layout = QVBoxLayout(self)
        layout.addWidget(self.generatedslave_label)
        layout.addWidget(self.slave_number_label)

    def nextId(self) -> int:
        return 11

class OpenWalletFile(QtWidgets.QWizardPage):
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
        return 11

class OpenWalletFileSlaves(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Open wallet file")

        self.password_qlabel = QLabel("Password (optional):")
        self.passwordline_edit = QLineEdit()
        self.passwordline_edit.setEchoMode(2)
        self.passwordline_edit.setPlaceholderText("Enter password")
        self.openFileBtn = QPushButton("Import secure wallet file")
        self.warning_label = QLabel("After clicking 'Next' button to begin, the slaves will be generated which will\ntake about 10 minutes. See the console for progress.\n\nPlease be patient.")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.password_qlabel)
        layout.addWidget(self.passwordline_edit)
        layout.addWidget(self.openFileBtn)
        layout.addWidget(self.warning_label)
        self.setLayout(layout)

    def nextId(self) -> int:
        return 8

class RegExpValidator(QtGui.QRegularExpressionValidator):
    validationChanged = QtCore.pyqtSignal(QtGui.QValidator.State)

    def validate(self, input, pos):
        state, input, pos = super().validate(input, pos)
        self.validationChanged.emit(state)
        return state, input, pos

class RestoreWallet(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Restore your wallet")

        self.seed_label = QLabel("Enter your seed:")
        self.seedline_edit = QLineEdit()
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.seed_label)
        layout.addWidget(self.seedline_edit)

        regexp_mnemonic = QtCore.QRegularExpression(r'((\b|\s)+\w+(\b|\s)+){34}|.{102}') #QRL address regex
        
        validator = RegExpValidator(regexp_mnemonic, self)
        validator.validationChanged.connect(self.handleValidationChange)
        self.seedline_edit.setValidator(validator)


    def handleValidationChange(self, state):
        if state == QtGui.QValidator.Invalid:
            colour = 'red'
        elif state == QtGui.QValidator.Intermediate:
            colour = 'gold'
        elif state == QtGui.QValidator.Acceptable:
            colour = 'lime'
        self.seedline_edit.setStyleSheet('border: 1px solid %s' % colour)

    def nextId(self) -> int:
        return 11

class RestoreWalletSlaves(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Restore your wallet")

        self.seed_label = QLabel("Enter your seed:")
        self.seedline_edit = QLineEdit()
        self.warning_label = QLabel("After clicking 'Next' button to begin, the slaves will be generated which will\ntake about 10 minutes. See the console for progress.\n\nPlease be patient.")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.seed_label)
        layout.addWidget(self.seedline_edit)
        layout.addWidget(self.warning_label)

        regexp_mnemonic = QtCore.QRegularExpression(r'((\b|\s)+\w+(\b|\s)+){34}|.{102}') #QRL address regex
        
        validator = RegExpValidator(regexp_mnemonic, self)
        validator.validationChanged.connect(self.handleValidationChange)
        self.seedline_edit.setValidator(validator)


    def handleValidationChange(self, state):
        if state == QtGui.QValidator.Invalid:
            colour = 'red'
        elif state == QtGui.QValidator.Intermediate:
            colour = 'gold'
        elif state == QtGui.QValidator.Acceptable:
            colour = 'lime'
        self.seedline_edit.setStyleSheet('border: 1px solid %s' % colour)

    def nextId(self) -> int:
        return 8


class LastPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Success!")

class QrlWallet(QtWidgets.QMainWindow, Ui_mainWindow, Ui_Form, Ui_Form2 , QtWidgets.QWizard, QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.model = Model()

        regexp_fee =  QRegExp(r'[0-9]+|([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?')
        regexp_ots_key = QRegExp(r'^[0-9]*$')
        self.fee_validator = QRegExpValidator(regexp_fee)
        self.ots_key_validator = QRegExpValidator(regexp_ots_key)

        header = self.transaction_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.send_button.clicked.connect(self.button_clicked)
        self.actionAbout.triggered.connect(self.about_popup)
        self.view_recovery_seed_btn.clicked.connect(self.recovery_seed_pop_up)
        self.actionCheck_for_updates.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/successor1/qrllight/releases")))
        self.actionOfficial_website.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://theqrl.org")))
        self.actionDocumentation.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://docs.theqrl.org/")))
        self.actionQRL_whitepaper.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://raw.githubusercontent.com/theQRL/Whitepaper/master/QRL_whitepaper.pdf")))
        self.actionReport_bug.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/successor1/qrllight/issues")))
        self.actionDonate_to_development.triggered.connect(self.donate_popup)

    def button_clicked(self):
        qrl_address = []
        mnemonic = []
        hexseed = []
        if QWizard.hasVisitedPage(main, 2):
            qrl_address.append(main.walletDetails.qaddress.toPlainText())
            mnemonic.append(main.walletDetails.mnemonic.text().rstrip())
            hexseed.append(main.walletDetails.hexseed.text())
        elif QWizard.hasVisitedPage(main, 5):
            qrl_address.append(main.data[0].split(" ")[0])
            mnemonic.append(" ".join(main.data[0].split(" ")[1:-1]))
            hexseed.append(main.data[0].split(" ")[35])
        elif QWizard.hasVisitedPage(main, 6):
            if main.restoreWallet.seedline_edit.text()[:6] ==  "absorb":
                qrl_address.append(Model.recoverAddressMnemonic(main.restoreWallet.seedline_edit.text()))
                mnemonic.append(main.restoreWallet.seedline_edit.text())
                hexseed.append(Model.recoverHexseedMnemonic(main.restoreWallet.seedline_edit.text()))
            elif main.restoreWallet.seedline_edit.text()[:2] ==  "01":
                qrl_address.append(Model.recoverAddressHexseed(main.restoreWallet.seedline_edit.text()))
                mnemonic.append(Model.recoverMnemonicHexseed(main.restoreWallet.seedline_edit.text()))
                hexseed.append(main.restoreWallet.seedline_edit.text())
        elif QWizard.hasVisitedPage(main, 3):
            qrl_address.append(main.walletDetailsExperimental.qaddress.toPlainText())
            mnemonic.append(main.walletDetailsExperimental.mnemonic.text().rstrip())
            hexseed.append(main.walletDetailsExperimental.hexseed.text())
        fee_validator = self.fee_validator.validate(self.fee_input.text(), 0)
        ots_key_validator = self.ots_key_validator.validate(self.ots_key_index_input.text(), 0)

        if fee_validator[0] != 2:
            QMessageBox.warning(self, "Warning: Incorrect Input!", "Wrong or empty fee input")
        elif ots_key_validator[0] != 2:
            QMessageBox.warning(self, "Warning: Incorrect Input!", "Wrong or empty OTS key input")
        else:
            remove_first_char_addrs = [e[1:] for e in self.send_input.text().split()]
            amount_string = self.amount_input.text().split()
            amount_int = map(int, amount_string)
            amount_list = [float(i) for i in list(amount_string)]
            addrs_to = remove_first_char_addrs
            amounts = amount_list
            message_data = self.description_input.text().encode() if self.description_input.text() else None
            fee = str(float(self.fee_input.text()) * 1000000000)[:-2]
            xmss_pk = XMSS.from_extended_seed(hstr2bin(hexseed[0])).pk
            src_xmss = XMSS.from_extended_seed(hstr2bin(hexseed[0]))
            ots_key = int(self.ots_key_index_input.text())
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Do you want to proceed?")
            msg.setInformativeText("Send to: " + self.send_input.text()  +"\nAmount: " + self.amount_input.text() + "\nFee: " + self.fee_input.text() + "\nOTS Key Index: " + self.ots_key_index_input.text())
            msg.setWindowTitle("QRL Confirmation")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            returnValue = msg.exec()
            if returnValue == QMessageBox.Cancel:
                pass
            else:
                models.TransferTransaction.tx_transfer(
                    addrs_to,
                    amounts,
                    message_data,
                    fee,
                    xmss_pk,
                    src_xmss,
                    ots_key)
                QMessageBox.about(self, "Succesful transaction", "Sent!")

    def update(self):
        self.balance_label.adjustSize()

    def about_popup(self):
        self.dialog=QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.dialog)
        self.dialog.show()
    
    def recovery_seed_pop_up(self):
        self.t = recoveryWindow
        self.t.show()

    def donate_popup(self):
        self.dialog=QtWidgets.QMainWindow()
        self.ui = Ui_Form2()
        self.ui.setupUi(self.dialog)
        self.dialog.show()

class RecoverySeedView(QWidget):
    def __init__(self):
        super(RecoverySeedView, self).__init__()
        self.setWindowTitle("Wallet details")
        self.warning_label = QLabel('Warning: If someone unauthorized gains access to these, your funds will be lost!', self )
        myFont=QtGui.QFont()
        self.warning_label.setAlignment(Qt.AlignCenter)
        self.warning_label.setStyleSheet('color: red')
        myFont.setBold(True)
        self.warning_label.setFont(myFont)
        self.mnemonic_label = QLabel('Mnemonic phrase', self )
        self.mnemonic_label.setAlignment(Qt.AlignCenter)
        self.mnemonic_label_text = QLabel()
        self.mnemonic_label_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.hexseed_label = QLabel('Hexseed', self )
        self.hexseed_label.setAlignment(Qt.AlignCenter)
        self.hexseed_label_text = QLabel()
        self.hexseed_label_text.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.mnemonic_label_text.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.mnemonic_label_text.setFrameShadow(QFrame.Plain)
        self.mnemonic_label_text.setLineWidth(1)
        self.mnemonic_label_text.setWordWrap(True)

        self.hexseed_label_text.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.hexseed_label_text.setFrameShadow(QFrame.Plain)
        self.hexseed_label_text.setLineWidth(1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.warning_label)
        layout.addWidget(self.mnemonic_label)
        layout.addWidget(self.mnemonic_label_text)
        layout.addWidget(self.hexseed_label)
        layout.addWidget(self.hexseed_label_text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MyWizard()
    mainWindow = QrlWallet()
    recoveryWindow = RecoverySeedView()
    app.setWindowIcon(QtGui.QIcon('logocircle.ico'))
    main.hide()
    main.setWindowModality(QtCore.Qt.ApplicationModal)
    mainWindow.show()
    main.show()
    sys.exit(app.exec_())

from views.view_ui import Ui_mainWindow
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from views.view_ui import Ui_mainWindow
import sys
from models.model import Model

class QrlWallet(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.model = Model()

        self.send_button.clicked.connect(self.button_clicked)


    def button_clicked(self):
        self.balance_label.setText("you pressed the button")
        self.update()

    def update(self):
        self.balance_label.adjustSize()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QrlWallet()
    mainWindow.show()
    sys.exit(app.exec_())

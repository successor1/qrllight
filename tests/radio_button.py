from PyQt5.QtWidgets import *
import sys

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        radiobutton = QRadioButton("Australia")
        radiobutton.country = "Australia"
        radiobutton.toggled.connect(self.onClicked)
        layout.addWidget(radiobutton, 1, 2)

        radiobutton = QRadioButton("China")
        radiobutton.country = "China"
        radiobutton.toggled.connect(self.onClicked)
        layout.addWidget(radiobutton, 2, 2)

        radiobutton = QRadioButton("Japan")
        radiobutton.country = "Japan"
        radiobutton.toggled.connect(self.onClicked)
        layout.addWidget(radiobutton, 3, 2)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Country is %s" % (radioButton.country))

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import *

class Window(QWizard):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.firstPage = MainPage()
        self.secondPage = Page2()

        self.addPage(self.firstPage)
        self.addPage(self.secondPage)


class MainPage(QWizardPage):
    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)

        self.setTitle("Plz input your name?")

        self.NameLabel = QLabel("&Name:")
        self.NameLineEdit = QLineEdit()
        self.NameLabel.setBuddy(self.NameLineEdit)

        layout = QHBoxLayout(self)
        layout.addWidget(self.NameLabel)
        layout.addWidget(self.NameLineEdit)

        self.registerField("my_name", self.NameLineEdit)


class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)

        vbox = QVBoxLayout(self)
        self.label = QLabel()
        vbox.addWidget(self.label)

    def initializePage(self):
        self.label.setText(f'My name is : {self.field("my_name")}')
        super(Page2, self).initializePage()

def main():
    app = QApplication(sys.argv)
    app.setStyle('plastique')

    window = Window()
    window.setWizardStyle(1)
    window.show()
    app.exec_()

if __name__ == "__main__":
    sys.exit(main())
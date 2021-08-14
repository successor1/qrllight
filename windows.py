from PyQt5 import QtWidgets

class MyWizard(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.checkBox = QtWidgets.QCheckBox('check')
        layout.addWidget(self.checkBox)
        self.input = QtWidgets.QLineEdit()
        layout.addWidget(self.input)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def setData(self, **data):
        self.checkBox.setChecked(data.get('check', False))
        self.input.setText(data.get('text', ''))

    def getData(self):
        return {'check': self.checkBox.isChecked(), 'text': self.input.text()}

    def exec_(self, **data):
        self.setData(**data)
        return super().exec_()


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        layout = QtWidgets.QHBoxLayout()
        centralWidget.setLayout(layout)
        self.showWizBtn = QtWidgets.QPushButton('Show wizard')
        self.btn = QtWidgets.QPushButton('Push button')
        layout.addWidget(self.showWizBtn)
        layout.addWidget(self.btn)
        self.showWizBtn.clicked.connect(self.getDataFromWizard)
        self.btn.clicked.connect(self.getPrint)
        self.data = {}

    def getDataFromWizard(self):
        wiz = MyWizard(self)
        if wiz.exec_(**self.data):
            self.data.update(wiz.getData())

    def getPrint(self, **data):
        print(MyWizard.checkbox.isChecked())


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

from common import *


class CustomPointsValueWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.mainLayout = QVBoxLayout()
        self.inputForm = QHBoxLayout()

        self.inputLabel = QLineEdit()
        self.plusMinus = QComboBox()
        self.plusMinus.addItems(["+", "-"])
        self.numberLabel = QLabel("Please provide the amount of points you would like to add/subtract: ")
        self.submitButton = QPushButton("Add/Subtract Points")

        self.inputForm.addWidget(self.numberLabel)
        self.inputForm.addWidget(self.inputLabel)
        self.inputForm.addWidget(self.plusMinus)

        self.mainLayout.addLayout(self.inputForm)
        self.mainLayout.addWidget(self.submitButton)

        self.setLayout(self.mainLayout)
        self.setColorPalette()

    def setColorPalette(self):
        data = loadJSONData()
        colorPalette = data["savedColorPalette"]
        with open(f'Color Palettes/{colorPalette}.css') as stylesheet:
            style = stylesheet.read()
        self.setStyleSheet(style)


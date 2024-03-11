from common import *


class CustomPointsValueWidget(QWidget):
    pointsChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.mainLayout = QVBoxLayout()
        self.inputForm = QHBoxLayout()

        self.inputLabel = QLineEdit()
        self.plusMinus = QComboBox()
        self.plusMinus.addItems(["+", "-"])
        self.plusMinus.setStyleSheet(setColorPalletForComboBox())
        self.numberLabel = QLabel("Please provide the amount of points you would like to add/subtract: ")
        self.submitButton = QPushButton("Add/Subtract Points")

        # connect button to function
        self.submitButton.clicked.connect(self.adjustPointValue)

        self.inputForm.addWidget(self.numberLabel)
        self.inputForm.addWidget(self.inputLabel)
        self.inputForm.addWidget(self.plusMinus)

        self.mainLayout.addLayout(self.inputForm)
        self.mainLayout.addWidget(self.submitButton)

        self.setLayout(self.mainLayout)
        setStyle(self, loadColorPallet())


    def adjustPointValue(self):
        data = loadJSONData()
        totalPointsNumber = data['numberOfPoints']
        completeNumber = f'{self.plusMinus.currentText()}{self.inputLabel.text()}'

        totalPointsNumber += int(completeNumber)
        data['numberOfPoints'] = totalPointsNumber
        updateJSONData(data)
        self.pointsChanged.emit(totalPointsNumber)





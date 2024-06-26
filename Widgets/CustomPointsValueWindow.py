from common import *

class CustomPointsValueWidget(QWidget):
    pointsChangedSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.mainLayout = QVBoxLayout()
        self.inputForm = QHBoxLayout()

        self.inputLabel = QLineEdit()
        self.plusMinus = QComboBox()
        self.plusMinus.addItems(["Add (+)", "Subtract (-)"])
        self.plusMinus.setStyleSheet(setColorPalletForComboBox(loadColorPallet()))
        self.numberLabel = QLabel("Input the number of points you would like to add/subtract: ")
        self.submitButton = QPushButton("Add/Subtract Points")

        # connect button to function
        self.submitButton.clicked.connect(self.adjustPointValue)

        self.inputForm.addWidget(self.numberLabel)
        self.inputForm.addWidget(self.inputLabel)
        self.inputForm.addWidget(self.plusMinus)

        self.mainLayout.addLayout(self.inputForm)
        self.mainLayout.addWidget(self.submitButton)

        self.setLayout(self.mainLayout)

    def processInteger(self):
        if self.plusMinus.currentText() == "Add (+)":
            return "+"
        elif self.plusMinus.currentText() == "Subtract (-)":
            return "-"

    def adjustPointValue(self):
        data = loadJSONData()
        totalPointsNumber = data['numberOfPoints']

        completeNumber = f'{self.processInteger()}{self.inputLabel.text()}'

        totalPointsNumber += int(completeNumber)
        data['numberOfPoints'] = totalPointsNumber
        updateJSONData(data)

        if self.confirmPointAdjustment(completeNumber):
            self.pointsChangedSignal.emit()
            showProcessConfirmationWindow("Point adjustment")

    def confirmPointAdjustment(self, numberOfPoints):
        integerValue = ''
        toOrFrom = ''
        if int(numberOfPoints) < 0:
            integerValue = "subtract"
            toOrFrom = "from"
        else:
            integerValue = "add"
            toOrFrom = "to"


        removedSign = abs(int(numberOfPoints))

        confirmPointAdjustmentWindow = QMessageBox()
        confirmPointAdjustmentWindow.setText(
            f"Would you like to {integerValue} {removedSign} points {toOrFrom} your total score?")
        confirmPointAdjustmentWindow.setWindowTitle("Confirm Point Adjustment")
        confirmPointAdjustmentWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = confirmPointAdjustmentWindow.exec_()

        if returnValue == QMessageBox.Yes:
            logProcess(f"Adjusted point total value by {numberOfPoints}")
            self.inputLabel.clear()
            return True
        if returnValue == QMessageBox.No:
            return False

    def applyIndividualStyling(self, palette):
        self.plusMinus.setStyleSheet(setColorPalletForComboBox(palette))
        self.inputLabel.setStyleSheet(setColorForInputLines(palette))

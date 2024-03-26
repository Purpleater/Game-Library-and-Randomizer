from common import *


# this is just a spare file that I use to test out a variety of features


def confirmPointAdjustment(numberOfPoints):
    integerValue = ''
    toOrFrom = ''
    if int(numberOfPoints) < 0:
        integerValue = "subtract"
        toOrFrom = "from"
    else:
        integerValue = "add"
        toOrFrom = "to"

    splitList = list(numberOfPoints)
    removedSign = splitList.pop(1)

    confirmPointAdjustmentWindow = QMessageBox()
    confirmPointAdjustmentWindow.setText(
        f"Would you like to {integerValue} {removedSign} points {toOrFrom} your total score?")
    confirmPointAdjustmentWindow.setWindowTitle("Confirm Point Adjustment")
    confirmPointAdjustmentWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    returnValue = confirmPointAdjustmentWindow.exec_()

    if returnValue == QMessageBox.Yes:
        return True
    if returnValue == QMessageBox.No:
        return False


confirmPointAdjustment("-5")

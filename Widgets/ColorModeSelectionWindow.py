from common import *
from PyQt5.QtCore import pyqtSignal

class ColorSelectionWindow(QWidget):
    colorSelection = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.mainLayout = QVBoxLayout()
        self.clickButton = QPushButton("Click me to change color palette")
        self.clickButton.clicked.connect(self.showColorDialog)

        # set widgets into layout
        self.mainLayout.addWidget(self.clickButton)

        self.setLayout(self.mainLayout)

    def showColorDialog(self):

        selectedPalette = self.getColorFromDialog()

        if selectedPalette:
            self.colorSelection.emit(selectedPalette)

    def getColorFromDialog(self):
        return "contrast"
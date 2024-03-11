import Widgets.CustomPointsValueWindow
from common import *
from PyQt5.QtCore import pyqtSignal


class ColorSelectionWindow(QWidget):
    paletteList = ["Contrast", "Sunset"]
    colorSelection = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        # layout creation
        self.mainLayout = QVBoxLayout()

        # create widgets
        self.palettelistSelection = QListWidget()
        self.clickButton = QPushButton("Test Color Palette")
        self.clickButton.clicked.connect(self.showColorDialog)

        # set widgets into layout
        self.mainLayout.addWidget(self.palettelistSelection)
        for i in range(len(self.paletteList)):
            self.palettelistSelection.addItem(self.paletteList[i])

        self.mainLayout.addWidget(self.clickButton)
        setStyle(self, loadColorPallet())
        self.setLayout(self.mainLayout)


    def showColorDialog(self):

        selectedPalette = self.getColorFromList()

        if selectedPalette:
            self.colorSelection.emit(selectedPalette)
        with open(f'Color Palettes/{selectedPalette}.css') as stylesheet:
            style = stylesheet.read()
            self.setStyleSheet(style)
            Widgets.CustomPointsValueWindow.CustomPointsValueWidget().setStyleSheet(style)


    def getColorFromList(self):
        return self.palettelistSelection.selectedItems()[0].text()



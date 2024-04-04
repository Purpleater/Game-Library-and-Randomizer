import Widgets.CustomPointsValueWindow
import common
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
        self.savePaletteButton = QPushButton("Save Applied Palette")
        self.savePaletteButton.clicked.connect(self.saveAppliedPalette)

        # set widgets into layout
        self.mainLayout.addWidget(self.palettelistSelection)
        for i in range(len(self.paletteList)):
            self.palettelistSelection.addItem(self.paletteList[i])

        self.mainLayout.addWidget(self.clickButton)
        self.mainLayout.addWidget(self.savePaletteButton)
        self.setLayout(self.mainLayout)


    def showColorDialog(self):

        selectedPalette = self.palettelistSelection.selectedItems()[0].text()
        common.currentlyAppliedColorScheme = selectedPalette
        if selectedPalette:
            self.colorSelection.emit(selectedPalette)
        with open(f'Color Palettes/{selectedPalette}.css') as stylesheet:
            style = stylesheet.read()
            self.setStyleSheet(style)
            Widgets.CustomPointsValueWindow.CustomPointsValueWidget().setStyleSheet(style)

    def saveAppliedPalette(self):
        data = loadJSONData()
        data['savedColorPalette'] = common.currentlyAppliedColorScheme.lower()
        updateJSONData(data)
        logProcess("Saved currently applied palette")

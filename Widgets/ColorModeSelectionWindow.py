import common
from common import *
from PyQt5.QtCore import pyqtSignal


class ColorSelectionWindow(QWidget):
    colorSelection = pyqtSignal(str)
    addStyleSheetWindowSignal = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):

        self.paletteList = self.loadPaletteList()
        # layout creation
        self.mainLayout = QVBoxLayout()

        # create widgets
        self.palettelistSelection = QListWidget()
        self.clickButton = QPushButton("Test Color Palette")
        self.clickButton.clicked.connect(self.showColorDialog)
        self.savePaletteButton = QPushButton("Save Applied Palette")
        self.savePaletteButton.clicked.connect(self.saveAppliedPalette)
        self.addCustomFile = QPushButton("Add custom stylesheet")
        self.addCustomFile.clicked.connect(self.addCustomStyleSheet)

        # set widgets into layout
        self.mainLayout.addWidget(self.palettelistSelection)
        for i in range(len(self.paletteList)):
            self.palettelistSelection.addItem(self.paletteList[i])

        self.mainLayout.addWidget(self.clickButton)
        self.mainLayout.addWidget(self.savePaletteButton)
        self.mainLayout.addWidget(self.addCustomFile)

        self.setLayout(self.mainLayout)


    def showColorDialog(self):

        selectedPalette = self.palettelistSelection.selectedItems()[0].text()
        common.currentlyAppliedColorScheme = selectedPalette
        if selectedPalette:
            self.colorSelection.emit(selectedPalette)
        logProcess(f"Temporarily applied the ({selectedPalette}) palette")

    def saveAppliedPalette(self):
        data = loadJSONData()
        data['savedColorPalette'] = common.currentlyAppliedColorScheme.lower()
        updateJSONData(data)
        logProcess("Saved currently applied palette")
        closeWindowRequest("Color palette save", self)

    def addCustomStyleSheet(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if fileName.endswith(".css"):
            self.addCustomStylesheetConfirmationWindow(fileName.split("/")[-1])
            printMeese()
        else:
            print("Booo, this isn't a css file")

    def showCustomStyleSheetNameInputWindow(self):
        self.addStyleSheetWindowSignal.emit()

    def addCustomStylesheetConfirmationWindow(self, selectedFile):
        stylesheetConfirmationWindow = QMessageBox()
        stylesheetConfirmationWindow.setText(f"Would you like to add [{selectedFile}]")
        stylesheetConfirmationWindow.setWindowTitle("Custom stylesheet submission confirmation")
        stylesheetConfirmationWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = stylesheetConfirmationWindow.exec_()

        if returnValue == QMessageBox.Yes:
            self.showCustomStyleSheetNameInputWindow()
        if returnValue == QMessageBox.No:
            printMeese()

    def loadPaletteList(self):
        data = loadJSONData()
        paletteList = data["colorPaletteList"]
        return paletteList

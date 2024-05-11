import common
from common import *


def returnToMainMenuRequest(process, returnMethod):
    closeRequestWindow = QMessageBox()
    closeRequestWindow.setText(f"{process} successful, would you like to return to the main menu?")
    closeRequestWindow.setWindowTitle("Process Successful")
    closeRequestWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    returnValue = closeRequestWindow.exec_()

    if returnValue == QMessageBox.Yes:
        returnMethod()
    if returnValue == QMessageBox.No:
        return

# the only reason I'm adding multiple classes here is because I"m experimenting with stacked widgets
# that and also these menus are going to be hidden within the main layout anyways so it makes sense that I would consolidate related components

# __MAIN MENU LAYOUT__
class MainMenu(QWidget):
    showColorPaletteButtonSignal = pyqtSignal()
    closeMenuSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.MenuInterface()

    def MenuInterface(self):
        # initialize main layout
        self.mainLayout = QVBoxLayout()

        # initialize buttons
        self.colorPaletteButton = QPushButton("Change UI Color Theme")
        self.toggleWidgetsButton = QPushButton("Toggle Application Widgets")
        self.resetAllDataButton = QPushButton("Reset All Save Data")
        self.closeWindowButton = QPushButton("Close Window")

        # connect buttons
        self.colorPaletteButton.clicked.connect(self.showColorPaletteMenu)
        self.closeWindowButton.clicked.connect(self.closeWindow)
        self.resetAllDataButton.clicked.connect(self.deleteDataProcess)

        # add widgets to main layout
        self.mainLayout.addWidget(self.colorPaletteButton)
        self.mainLayout.addWidget(self.toggleWidgetsButton)
        self.mainLayout.addWidget(self.resetAllDataButton)
        self.mainLayout.addWidget(self.closeWindowButton)

        # set main layout
        self.setLayout(self.mainLayout)

    def showColorPaletteMenu(self):
        self.showColorPaletteButtonSignal.emit()

    def closeWindow(self):
        self.closeMenuSignal.emit()

    def deleteDataProcess(self):
        if self.showFirstResetValidation():
            printMeese()

    def showFirstResetValidation(self):
        firstResetValidationWindow = QMessageBox()
        firstResetValidationWindow.setText(f"Would you like to reset all of the application's data? This will include games, points, visual preferences, etc.")
        firstResetValidationWindow.setWindowTitle("Reset Validation")
        firstResetValidationWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = firstResetValidationWindow.exec_()

        if returnValue == QMessageBox.Yes:
            return True
        if returnValue == QMessageBox.No:
            return False


# __COLOR MENU LAYOUT__
class ColorWidgetMenu(QWidget):
    returnToMainMenuSignal = pyqtSignal()
    testColorTheme = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.MenuInterface()

    def MenuInterface(self):
        self.mainLayout = QVBoxLayout()
        self.palettelistSelection = QListWidget()
        self.loadThemeList()

        self.testColorPaletteButton = QPushButton("Test Color Palette")
        self.testColorPaletteButton.clicked.connect(self.testColorPalette)
        self.savePaletteButton = QPushButton("Save Currently-Applied Palette")
        self.savePaletteButton.clicked.connect(self.saveAppliedPalette)
        self.addCustomFile = QPushButton("Add Custom Stylesheet")
        self.returnToMenuButton = QPushButton("Return To Main Menu")

        self.returnToMenuButton.clicked.connect(self.returnToMainMenu)

        self.mainLayout.addWidget(self.palettelistSelection)
        self.mainLayout.addWidget(self.testColorPaletteButton)
        self.mainLayout.addWidget(self.savePaletteButton)
        self.mainLayout.addWidget(self.addCustomFile)
        self.mainLayout.addWidget(self.returnToMenuButton)

        self.setLayout(self.mainLayout)

    def returnToMainMenu(self):
        self.returnToMainMenuSignal.emit()

    def testColorPalette(self):
        selectedPalette = self.palettelistSelection.selectedItems()[0].text()
        common.currentlyAppliedColorScheme = selectedPalette
        if selectedPalette:
            self.testColorTheme.emit(selectedPalette)
        logProcess(f"Temporarily applied the ({selectedPalette}) palette")

    def loadThemeList(self):
        data = loadJSONData()
        paletteList = data["colorPaletteList"]
        self.mainLayout.addWidget(self.palettelistSelection)
        for i in range(len(paletteList)):
            self.palettelistSelection.addItem(paletteList[i])

    def saveAppliedPalette(self):
        data = loadJSONData()
        data['savedColorPalette'] = common.currentlyAppliedColorScheme.lower()
        updateJSONData(data)
        logProcess("Saved currently applied palette")
        returnToMainMenuRequest("Save", self.returnToMainMenu)


class OptionsMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        # initialize main layout
        self.mainLayout = QStackedLayout()
        # import individual menus into class
        self.mainMenu = MainMenu()
        self.colorThemeMenu = ColorWidgetMenu()

        # set signal slots
        self.mainMenu.showColorPaletteButtonSignal.connect(self.showColorThemeMenu)

        # color options menu slots
        self.colorThemeMenu.returnToMainMenuSignal.connect(self.showMainMenu)

        # stack menus
        self.mainLayout.addWidget(self.mainMenu)
        self.mainLayout.addWidget(self.colorThemeMenu)

        # set main layout
        self.setLayout(self.mainLayout)

    def showMainMenu(self):
        self.mainLayout.setCurrentIndex(0)
        logProcess("Loaded main menu")

    def showColorThemeMenu(self):
        self.mainLayout.setCurrentIndex(1)
        logProcess("Loaded UI-adjustment menu")


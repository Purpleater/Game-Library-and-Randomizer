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

    def __init__(self):
        super().__init__()
        self.MenuInterface()

    def MenuInterface(self):
        # initialize main layout
        self.mainLayout = QVBoxLayout()

        # initialize buttons
        self.colorPaletteButton = QPushButton("Change UI Color Theme")
        self.toggleWidgetsButton = QPushButton("Toggle Application Widgets")
        self.closeWindowButton = QPushButton("Close Window")

        # connect buttons
        self.colorPaletteButton.clicked.connect(self.showColorPaletteMenu)

        # add widgets to main layout
        self.mainLayout.addWidget(self.colorPaletteButton)
        self.mainLayout.addWidget(self.toggleWidgetsButton)
        self.mainLayout.addWidget(self.closeWindowButton)

        # set main layout
        self.setLayout(self.mainLayout)

    def showColorPaletteMenu(self):
        self.showColorPaletteButtonSignal.emit()

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
        # ADD CUSTOM STYLESHEET CONNECTION
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


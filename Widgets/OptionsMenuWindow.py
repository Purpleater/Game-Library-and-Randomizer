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
    showToggleWidgetsWindowSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.MenuInterface()

    def MenuInterface(self):

        # import other classes
        self.secondResetValidation = ResetAllDataConfirmationWindow()

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
        self.toggleWidgetsButton.clicked.connect(self.showToggleWidgetMenu)

        # connect signals
        self.secondResetValidation.confirmationSignal.connect(self.resetAllData)

        # add widgets to main layout
        self.mainLayout.addWidget(self.colorPaletteButton)
        self.mainLayout.addWidget(self.toggleWidgetsButton)
        self.mainLayout.addWidget(self.resetAllDataButton)
        self.mainLayout.addWidget(self.closeWindowButton)

        # set main layout
        self.setLayout(self.mainLayout)

    def showColorPaletteMenu(self):
        self.showColorPaletteButtonSignal.emit()

    def showToggleWidgetMenu(self):
        self.showToggleWidgetsWindowSignal.emit()

    def closeWindow(self):
        self.closeMenuSignal.emit()

    def deleteDataProcess(self):
        if self.showFirstResetValidation():
            self.showSecondResetValidation()

    def showFirstResetValidation(self):
        firstResetValidationWindow = QMessageBox()
        firstResetValidationWindow.setText(
            f"Would you like to reset all of the application's data? This will include games, points, visual preferences, etc.")
        firstResetValidationWindow.setWindowTitle("Reset Validation")
        firstResetValidationWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = firstResetValidationWindow.exec_()

        if returnValue == QMessageBox.Yes:
            return True
        if returnValue == QMessageBox.No:
            return False

    def showSecondResetValidation(self):
        self.secondResetValidation.setWindowTitle("Uber-Confirmation Window")
        self.secondResetValidation.show()

    def resetAllData(self):
        data = loadJSONData()

        '''
        RESET THE FOLLOWING: 
        - savedColorPalette (back to contrast, or some other bright styling) ✓
        - savedDate ✓ 
        - gameOfTheWeek ✓ (kinda)
        - rollgameList ✓
        - cardDrawList ✓
        - personalGameList
        - number of points
        - lastGameID 
        - fullGameList
        '''
        data["savedColorPalette"] = 'contrast'
        data["savedDate"] = datetime.now().strftime("%Y,%m,%d")
        data["fullGameList"] = []
        data["cardDrawList"] = []
        data["personalGameList"] = []

        for i in range(15):
            placeholderGame = {
                'name': f"PLACEHOLDER NAME {i + 1}",
                'id': i + 1,
                'completed': 'Incomplete',
                "replayabilityFactor": "Low"
            }
            data["fullGameList"].append(placeholderGame)
        data["lastGameID"] = 16

        # provide temporary placeholders for the roll game list
        data["rollGameList"] = []

        for i in range (20):
            data["rollGameList"].append(random.choice(data["fullGameList"])["name"])

        idList = []
        while len(idList) < 13:
            randomGame = random.choice(data["fullGameList"])

            if randomGame["id"] in idList or randomGame["id"] == -1:
                continue
            if randomGame["completed"] == "Complete":
                randomNum = random.randint(1, 4)
                gameReplayValue = replayabilityStatusReference[randomGame["replayabilityFactor"]]
                if gameReplayValue < randomNum:
                    continue
            idList.append(randomGame["id"])
        print(idList)
        for i in range(len(idList)):
            for game in data["fullGameList"]:
                if idList[i] == game["id"]:
                    data["cardDrawList"].append(game["name"])
        data["numberOfPoints"] = 0
        data["gameOfTheWeek"] = "¯\_(ツ)_/¯"

        print(data)



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

class ToggleWidgetsMenu(QWidget):
    returnToMainMenuSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.mainLayout = QVBoxLayout()

        # create widgets
        self.backButton = QPushButton("Return To Menu")

        # connections
        self.backButton.clicked.connect(self.returnToMainMenu)

        # add widgets
        self.mainLayout.addWidget(self.backButton)

        self.setLayout(self.mainLayout)

    def returnToMainMenu(self):
        self.returnToMainMenuSignal.emit()

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
        self.toggleWidgetsMenu = ToggleWidgetsMenu()


        # set signal slots
        self.mainMenu.showColorPaletteButtonSignal.connect(self.showColorThemeMenu)
        self.toggleWidgetsMenu.returnToMainMenuSignal.connect(self.showMainMenu)
        self.mainMenu.showToggleWidgetsWindowSignal.connect(self.showToggleWidgetsMenu)

        # color options menu slots
        self.colorThemeMenu.returnToMainMenuSignal.connect(self.showMainMenu)

        # stack menus
        self.mainLayout.addWidget(self.mainMenu)
        self.mainLayout.addWidget(self.colorThemeMenu)
        self.mainLayout.addWidget(self.toggleWidgetsMenu)

        # set main layout
        self.setLayout(self.mainLayout)

    def showMainMenu(self):
        self.mainLayout.setCurrentIndex(0)
        logProcess("Loaded main menu")

    def showColorThemeMenu(self):
        self.mainLayout.setCurrentIndex(1)
        logProcess("Loaded UI-adjustment menu")

    def showToggleWidgetsMenu(self):
        self.mainLayout.setCurrentIndex(2)
        logProcess("Loaded toggle widgets menu")



class ResetAllDataConfirmationWindow(QWidget):
    confirmationSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.mainLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.promptLabel = QLabel("Are you sure you want to reset this application's save data? \nType the 'cheeseburger' to confirm your decision.")
        self.decisionInput = QLineEdit()
        self.backButton = QPushButton("Back")
        self.submitButton = QPushButton("Submit")

        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.submitButton)

        self.mainLayout.addWidget(self.promptLabel)
        self.mainLayout.addWidget(self.decisionInput)
        self.mainLayout.addLayout(self.buttonLayout)

        # connect button
        self.submitButton.clicked.connect(self.checkInputValue)
        self.backButton.clicked.connect(self.hideWindow)

        self.setLayout(self.mainLayout)

    def checkInputValue(self):
        if self.decisionInput.text().lower() == 'cheeseburger':
            self.confirmationSignal.emit()

    def hideWindow(self):
        self.decisionInput.clear()
        self.hide()




from common import *


def showGameEditConfirmationWindow():
    promptString = "The game that you are trying to submit is already present within the list. Would you like to re-submit this information?"
    windowTitle = "Edit Game Confirmation"
    return createStandardConfirmationWindow(promptString, windowTitle, [windowLogProcess("Edit of game information complete")], [])


class EditGameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widgetUI()
        self.currentGameID = -1

    def widgetUI(self):


        self.mainLayout = QVBoxLayout()
        self.inputForm = QFormLayout()
        # this layout is to make sure that the name input field and the duplicate game check are on the same row
        self.gameNameLayout = QHBoxLayout()
        # this layout has a similar purpose to the previous one, except with searching for a game in the list
        self.searchGameRow = QHBoxLayout()

        # user input form widgets
        self.nameValue = QLineEdit()

        self.completionStatus = QComboBox()
        self.completionStatus.addItems(["Incomplete", "Complete", "No Ending"])
        self.completionStatus.setStyleSheet(setColorPalletForComboBox(loadColorPallet()))
        self.replayabilityFactor = QComboBox()
        self.replayabilityFactor.addItems(["Low", "Moderate", "High", "Very High"])
        self.replayabilityFactor.setStyleSheet(setColorPalletForComboBox(loadColorPallet()))
        self.submitInformation = QPushButton("Submit Game Information")
        self.checkForDuplicateButton = QPushButton("Duplicate Game Check")

        self.gameNameLayout.addWidget(self.nameValue)
        self.gameNameLayout.addWidget(self.checkForDuplicateButton)

        # individual labels are used because of eventual style sheet employment
        self.gNameLabel = QLabel("Game Name")
        self.gCompletedLabel = QLabel("Game Completed?")
        self.gReplayabilityLabel = QLabel("Game Replayability Factor (Select One)")

        self.inputForm.addRow(self.gNameLabel, self.gameNameLayout)
        self.inputForm.addRow(self.gCompletedLabel, self.completionStatus)
        self.inputForm.addRow(self.gReplayabilityLabel, self.replayabilityFactor)
        self.inputForm.addRow(self.submitInformation)

        # list to show all games present + search bar
        self.findGameInput = QLineEdit()
        self.findGameLabel = QLabel("Search For a Game")
        self.editGameSelectionList = QListWidget()
        self.populateList()
        self.selectGameToEditButton = QPushButton("Select Game to Edit/View")
        self.selectGameToEditButton.clicked.connect(self.getGameInformation)
        self.selectGameToEditButton.setEnabled(False)
        self.deleteGameButton = QPushButton("Delete Game")
        self.deleteGameButton.setEnabled(False)

        self.editGameSelectionList.itemSelectionChanged.connect(self.checkIfGameIsSelected)

        self.searchGameRow.addWidget(self.findGameLabel)
        self.searchGameRow.addWidget(self.findGameInput)

        # the list box will reflect the search results made in the search bar
        self.findGameInput.textChanged.connect(self.updateSearchedList)

        # connect buttons
        self.submitInformation.clicked.connect(self.submitFormInformation)
        self.checkForDuplicateButton.clicked.connect(self.duplicateGameCheck)
        self.deleteGameButton.clicked.connect(self.deleteGame)

        # set layouts
        self.mainLayout.addLayout(self.inputForm)
        self.mainLayout.addLayout(self.searchGameRow)
        self.mainLayout.addWidget(self.editGameSelectionList)
        self.mainLayout.addWidget(self.selectGameToEditButton)
        self.mainLayout.addWidget(self.deleteGameButton)
        self.setLayout(self.mainLayout)

        # the method that loads all of the games and adds them to the list

    def populateList(self):
        self.editGameSelectionList.clear()
        self.editGameSelectionList.addItem(
            "SELECT A GAME AND CLICK THE BUTTON BELOW TO VIEW THE CURRENT INFORMATION")
        for game in loadSortedList():
            self.editGameSelectionList.addItem(game["name"])


    def submitFormInformation(self):
        gameName = self.nameValue.text().strip()
        completionStatus = findDictionaryKey(completionStatusReference, self.completionStatus.currentIndex())
        replayabilityStatus = findDictionaryKey(replayabilityStatusReference, self.replayabilityFactor.currentIndex())

        validation = self.inputValidation()

        if validation == 1:
            completionStatus = findDictionaryKey(completionStatusReference, self.completionStatus.currentIndex())
            replayabilityStatus = findDictionaryKey(replayabilityStatusReference, self.replayabilityFactor.currentIndex())
            editExistingGameInformation(self.currentGameID, gameName, completionStatus, replayabilityStatus)
            self.populateList()
            self.resetPage()

        if validation == 2:
            newGame = Game(gameName, completionStatus, replayabilityStatus)
            updateFullGameList(newGame.toJSON())
            closeWindowRequest("Game submission", self)
            self.populateList()
            self.resetPage()
        if validation == 0:
            logProcess("Edit of pre-existing entry cancelled")
            return

    def getGameInformation(self):

        selectedItem = self.editGameSelectionList.selectedItems()[0].text()
        gameId = getIdByName(selectedItem)

        for game in loadSortedList():
            if gameId == game["id"]:
                self.nameValue.setText(selectedItem)
                self.completionStatus.setCurrentIndex(completionStatusReference[game["completed"]])
                self.replayabilityFactor.setCurrentIndex(replayabilityStatusReference[game["replayabilityFactor"]])
                self.currentGameID = gameId
                logProcess(f"The ID of the currently stored game is ({self.currentGameID})")
                break

    def updateSearchedList(self):
        self.editGameSelectionList.clear()
        for game in loadSortedList():
            if self.findGameInput.text().lower() in game["name"].lower():
                self.editGameSelectionList.addItem(game["name"])

    def resetPage(self):
        self.nameValue.clear()
        self.completionStatus.setCurrentIndex(0)
        self.replayabilityFactor.setCurrentIndex(0)
        self.findGameInput.clear()
        self.populateList()
        self.currentGameID = -1
        logProcess("Reset EditGamesWindow form")

    def inputValidation(self):
        inputFieldValue = self.nameValue.text()
        if len(inputFieldValue.strip()) == 0:
            QMessageBox.about(self, "Name Value Absent", "The Game Name field needs to be filled out.")
            return False

        # returning 1 means that the the game of the currently-stored id is to be edited
        # returning 2 means that the application should create an entirely new entry
        # returning 0 means that the function was cancelled
        if self.currentGameID != -1:
            if showGameEditConfirmationWindow():
                return 1
            else:
                return 0
        else:
            return 2

    def showGameDeletionConfirmationWindow(self, gameName):
        promptString = f"Would you like to delete {gameName}?"
        windowTitle = "Game Deletion Confirmation"
        return createStandardConfirmationWindow(promptString, windowTitle, [windowLogProcess(f"Deleted ({gameName})")], [])

    def duplicateGameCheck(self):
        gameName = self.nameValue.text().strip()
        if len(gameName) == 0:
            QMessageBox.about(self, "Name Value Absent", "The Game Name field needs to be filled out.")

        for game in loadSortedList():
            if gameName.lower() == game["name"].lower():
                QMessageBox.about(self, "Entry Already Present",
                                  "This game already exists within the program's files.")
                self.resetPage()

    def checkIfGameIsSelected(self):
        selectedItem = self.editGameSelectionList.selectedItems()
        if selectedItem:
            self.selectGameToEditButton.setEnabled(True)
            self.deleteGameButton.setEnabled(True)

    def applyIndividualStyling(self, palette):
        self.completionStatus.setStyleSheet(setColorPalletForComboBox(palette))
        self.replayabilityFactor.setStyleSheet(setColorPalletForComboBox(palette))
        self.nameValue.setStyleSheet(setColorForInputLines(palette))

    def deleteGame(self):
        selectedItem = self.editGameSelectionList.selectedItems()[0].text()
        data = loadJSONData()
        fullGameList = data["fullGameList"]
        for game in fullGameList:
            if game["name"] == selectedItem:
                if self.showGameDeletionConfirmationWindow(game["name"]):
                    fullGameList.remove(game)
                    updateJSONData(data)
                    showProcessConfirmationWindow("Game deletion")
                    self.resetPage()








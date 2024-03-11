from common import *


class EditGameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widgetUI()

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
        self.completionStatus.setStyleSheet(setColorPalletForComboBox())
        self.replayabilityFactor = QComboBox()
        self.replayabilityFactor.addItems(["Low", "Moderate", "High", "Very High"])
        self.replayabilityFactor.setStyleSheet(setColorPalletForComboBox())
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

        self.editGameSelectionList.itemSelectionChanged.connect(self.checkIfGameIsSelected)

        self.searchGameRow.addWidget(self.findGameLabel)
        self.searchGameRow.addWidget(self.findGameInput)

        # the list box will reflect the search results made in the search bar
        self.findGameInput.textChanged.connect(self.updateSearchedList)

        # connect buttons
        self.submitInformation.clicked.connect(self.submitFormInformation)
        self.checkForDuplicateButton.clicked.connect(self.duplicateGameCheck)
        # set layouts
        self.mainLayout.addLayout(self.inputForm)
        self.mainLayout.addLayout(self.searchGameRow)
        self.mainLayout.addWidget(self.editGameSelectionList)
        self.mainLayout.addWidget(self.selectGameToEditButton)
        self.setLayout(self.mainLayout)
        setStyle(self, loadColorPallet())

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


        if self.inputValidation() is not False:
            newGame = Game(gameName, completionStatus, replayabilityStatus)
            updateFullGameList(newGame.toJSON())
            showProcessConfirmationWindow("Game submission")
            self.populateList()
            self.resetPage()

    def getGameInformation(self):

        selectedItem = self.editGameSelectionList.selectedItems()[0].text()

        for game in loadSortedList():
            if selectedItem.lower() == game["name"].lower():
                self.nameValue.setText(selectedItem)
                self.completionStatus.setCurrentIndex(completionStatusReference[game["completed"]])
                self.replayabilityFactor.setCurrentIndex(replayabilityStatusReference[game["replayabilityFactor"]])

    def updateSearchedList(self):
        self.editGameSelectionList.clear()
        for game in loadSortedList():
            if self.findGameInput.text().lower() in game["name"].lower():
                self.editGameSelectionList.addItem(game["name"])

    def resetPage(self):
        self.nameValue.clear()
        self.completionStatus.setCurrentIndex(0)
        self.replayabilityFactor.setCurrentIndex(0)

    def inputValidation(self):
        inputFieldValue = self.nameValue.text()
        if len(inputFieldValue.strip()) == 0:
            QMessageBox.about(self, "Name Value Absent", "The Game Name field needs to be filled out.")
            return False
        for game in loadSortedList():
            if inputFieldValue.lower() == game["name"].lower():
                if self.showGameEditConfirmationWindow():
                    gameId = game["id"]
                    completionStatus = findDictionaryKey(completionStatusReference, self.completionStatus.currentIndex())
                    replayabilityStatus = findDictionaryKey(replayabilityStatusReference, self.replayabilityFactor.currentIndex())

                    editExistingGameInformation(gameId, completionStatus, replayabilityStatus)
                    return False
                else:
                    self.nameValue.clear()
                    return False


    def showGameEditConfirmationWindow(self):

        editGameConfirmationWindow = QMessageBox()
        editGameConfirmationWindow.setText("The game that you are trying to "
                                           "submit already is already present within the list. "
                                           "Would you like to re-submit this "
                                           "information?")
        editGameConfirmationWindow.setWindowTitle("Edit Game Confirmation")
        editGameConfirmationWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = editGameConfirmationWindow.exec_()

        if returnValue == QMessageBox.Yes:
            return True
        if returnValue == QMessageBox.No:
            return False

    def duplicateGameCheck(self):
        gameName = self.nameValue.text().strip()
        if len(gameName) == 0:
            QMessageBox.about(self, "Name Value Absent", "The Game Name field needs to be filled out.")

        for game in loadSortedList():
            if gameName.lower() == game["name"].lower():
                QMessageBox.about(self, "Duplicate Entry Warning",
                                  "The game you have provided "
                                  "already exists within the "
                                  "full game list.")
                self.resetPage()

    def checkIfGameIsSelected(self):
        selectedItem = self.editGameSelectionList.selectedItems()
        if selectedItem:
            self.selectGameToEditButton.setEnabled(True)






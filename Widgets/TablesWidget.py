from common import *
from Widgets.EditPersonalGameListWindow import EditPersonalGameListWindow
from Widgets.OptionsMenuWindow import MainMenu


class TablesWidget(QWidget):
    personalGamesButtonSignal = pyqtSignal()
    generateWeeklyGameSignal = pyqtSignal()
    saveWeeklyGameSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # initialize time-sensitive info Widget
        self.widgetUI()

    def widgetUI(self):

        self.optionsMenu = MainMenu()

        self.mainLayout = QVBoxLayout()
        self.tableLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.personalTableLayout = QVBoxLayout()

        # values containing the randomized information (for saving purposes)
        self.diceRollList = []
        self.cardDrawList = []
        self.gameOfTheWeek = ''

        # __TABLES LAYOUT__

        # Dice Roll Table Layout
        self.rollTableLayout = QVBoxLayout()
        self.rollTableLabel = QLabel("D20 Table")
        self.rollTableLabel.setAlignment(Qt.AlignCenter)

        self.rollTable = QTableWidget(20, 1, self)
        self.rollTable.setHorizontalHeaderLabels(["Game"])
        self.rollTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rollTable.setStyleSheet(setColorofTableCorner(loadColorPallet()))

        self.rollTableLayout.addWidget(self.rollTableLabel)
        self.rollTableLayout.addWidget(self.rollTable)

        # Card Draw Table Layout
        self.cardDrawTableLayout = QVBoxLayout()
        self.cardDrawTableLabel = QLabel("Card Draw Table")
        self.cardDrawTableLabel.setAlignment(Qt.AlignCenter)

        self.cardTable = QTableWidget(14, 2, self)
        self.cardTable.setHorizontalHeaderLabels(["Card", "Game"])
        self.cardTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.cardTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cardTable.setStyleSheet(setColorofTableCorner(loadColorPallet()))

        self.cardDrawTableLayout.addWidget(self.cardDrawTableLabel)
        self.cardDrawTableLayout.addWidget(self.cardTable)

        # load the card names for the card-draw table
        for i in range(14):
            rowName = QTableWidgetItem(f"{cardDeckNames[i]}")
            rowName.setFlags(rowName.flags() & Qt.ItemIsEditable)
            rowName.setForeground(QColor(Qt.black))
            self.cardTable.setItem(i, 0, rowName)

        # Personal Preference Table Layout

        self.personalTable = QTableWidget(12, 1, self)
        self.personalTable.setHorizontalHeaderLabels(["Game"])
        self.personalTable.setColumnWidth(0, 275)
        self.personalTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.personalTable.setStyleSheet(setColorofTableCorner(loadColorPallet()))

        self.personalTableLabel = QLabel("Games I Want To Continue Playing")
        self.personalTableLabel.setAlignment(Qt.AlignCenter)

        # I just decided to create the edit window here because it correlates with the personal preference table only
        self.editPersonalTableButton = QPushButton("Edit Want-To-Continue-Playing List")

        self.editPersonalGameListWindow = EditPersonalGameListWindow()
        self.editPersonalGameListWindow.setObjectName("editGamesListWindow")

        self.editPersonalTableButton.clicked.connect(self.showEditPersonalGamesWindow)

        # add widgets to table layout
        self.tableLayout.addLayout(self.rollTableLayout)
        self.tableLayout.addLayout(self.cardDrawTableLayout)

        self.personalTableLayout.addWidget(self.personalTableLabel)
        self.personalTableLayout.addWidget(self.personalTable)
        self.personalTableLayout.addWidget(self.editPersonalTableButton)

        # __BUTTON LAYOUT__

        self.rerollTables = QPushButton("Reroll Tables")
        self.saveTables = QPushButton("Save Table Info")

        # connect buttons
        self.rerollTables.clicked.connect(self.generateTableContents)
        self.saveTables.clicked.connect(self.otherSaveAllInformationFunction)

        # connect signal

        # add widgets to button layout
        self.buttonLayout.addWidget(self.rerollTables)
        self.buttonLayout.addWidget(self.saveTables)

        # add child layouts to main layout
        self.tableLayout.addLayout(self.personalTableLayout)
        self.mainLayout.addLayout(self.tableLayout)
        self.mainLayout.addLayout(self.buttonLayout)

        if detectIfEnoughTimeHasPassed():
            self.generateTableContents()
            self.saveAllInformation()
            replaceDate()
            self.loadStoredTables(loadSpecificList("rollGameList"), loadSpecificList("cardDrawList"))
            self.pingWeeklyGameReroll()
        else:
            self.loadStoredTables(loadSpecificList("rollGameList"), loadSpecificList("cardDrawList"))
            print("Data load successful")
            printNumberOfDaysLeft()

        # set main layout
        self.setLayout(self.mainLayout)

    def showEditPersonalGamesWindow(self):
        self.personalGamesButtonSignal.emit()

    def loadStoredTablesSignalMethod(self):
        self.loadStoredTables(loadSpecificList("rollGameList"), loadSpecificList("cardDrawList"))

    def loadStoredTables(self, diceList, cardList):

        for i in range(20):
            item = QTableWidgetItem(searchGameByID(diceList[i])["name"])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.rollTable.setItem(i, 0, item)

        for i in range(len(cardList)):
            item = QTableWidgetItem(searchGameByID(cardList[i])["name"])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.cardTable.setItem(i, 1, item)

        data = loadJSONData()
        loadedPersonalList = data['personalGameList']

        for i in range(len(loadedPersonalList)):
            item = QTableWidgetItem(searchGameByID(loadedPersonalList[i])["name"])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.personalTable.setItem(i, 0, item)

    def generateTableContents(self):
        self.diceRollList.clear()
        self.cardDrawList.clear()
        fullGameList = loadSortedList()

        # dice roll list

        while len(self.diceRollList) < 20:
            randomGame = random.choice(fullGameList)
            if len(self.diceRollList) == 19:
                self.diceRollList.append(-1)
                break

            if randomGame["completed"] == "Complete":
                randomNum = random.randint(1, 4)
                gameReplayValue = replayabilityStatusReference[randomGame["replayabilityFactor"]]
                if gameReplayValue > randomNum:
                    self.diceRollList.append(randomGame["id"])
                else:
                    continue
            else:
                self.diceRollList.append(randomGame["id"])

        for i in range(20):
            item = QTableWidgetItem(searchGameByID(self.diceRollList[i])["name"])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.rollTable.setItem(i, 0, item)

        # card draw list

        while len(self.cardDrawList) < 14:
            if len(self.cardDrawList) == 13:
                self.cardDrawList.append(-1)
                break
            randomGame = random.choice(fullGameList)
            if randomGame["id"] in self.cardDrawList or randomGame["id"] == -1:
                continue
            if randomGame["completed"] == "Complete":
                randomNum = random.randint(1, 4)
                gameReplayValue = replayabilityStatusReference[randomGame["replayabilityFactor"]]
                if gameReplayValue < randomNum:
                    continue

            self.cardDrawList.append(randomGame["id"])

        for i in range(14):
            item = QTableWidgetItem(searchGameByID(self.cardDrawList[i])["name"])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.cardTable.setItem(i, 1, item)
        self.pingWeeklyGameReroll()
        logProcess("New table contents generated")

    def saveAllInformation(self):
        data = loadJSONData()

        self.diceRollList = []
        self.cardDrawList = []

        for row in range(20):
            rollId = getIdByName(self.rollTable.item(row, 0).text())
            if rollId == None:
                self.diceRollList.append(-1)
            else:
                self.diceRollList.append(rollId)

        for row in range(14):
            drawId = getIdByName(self.cardTable.item(row, 1).text())
            if drawId == None:
                self.cardDrawList.append(-1)
            else:
                self.cardDrawList.append(drawId)

        data['rollGameList'] = self.diceRollList
        data['cardDrawList'] = self.cardDrawList
        updateJSONData(data)
        self.saveWeeklyGameSignal.emit()

        logProcess(f"Current information data set saved\n"
                   f"New Dice Roll ID Array: {self.diceRollList}\n"
                   f"New Card Draw ID Array: {self.cardDrawList}\n")



    def otherSaveAllInformationFunction(self):
        confirmationValidation = self.saveTableInformationConfirmationWindow()
        if confirmationValidation:
            self.saveAllInformation()

    def saveTableInformationConfirmationWindow(self):
        confirmationWindow = QMessageBox()
        confirmationWindow.setText(f"Would you like to save the information present on the tables?")
        confirmationWindow.setWindowTitle("Save Information Confirmation")
        confirmationWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = confirmationWindow.exec_()

        if returnValue == QMessageBox.Yes:
            showProcessConfirmationWindow("Saving of table information")
            return True
        if returnValue == QMessageBox.No:
            return False

    def applyIndividualStyling(self, palette):
        self.rollTable.setStyleSheet(setColorofTableCorner(palette))
        self.cardTable.setStyleSheet(setColorofTableCorner(palette))
        self.personalTable.setStyleSheet(setColorofTableCorner(palette))

    def loadPersonalList(self):
        data = loadJSONData()
        loadedPersonalList = data['personalGameList']

        for i in range(len(loadedPersonalList)):
            item = QTableWidgetItem(searchGameByID(loadedPersonalList[i])["name"])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.personalTable.setItem(i, 0, item)

    def pingWeeklyGameReroll(self):
        self.generateWeeklyGameSignal.emit()
        print("this is pinging the weekly game reroll")
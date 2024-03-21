from common import *
from Widgets.EditPersonalGameListWindow import EditPersonalGameListWindow


class TablesWidget(QWidget):
    personalGamesButtonSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        # initialize time-sensitive info Widget
        self.widgetUI()

    def widgetUI(self):

        self.mainLayout = QVBoxLayout()
        self.tableLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.personalTableLayout = QVBoxLayout()

        # values containing the randomized information (for saving purposes)
        self.diceRollList = []
        self.cardDrawList = []
        self.gameOfTheWeek = ''

        # __TABLES LAYOUT__

        # Dice Roll Table
        self.rollTable = QTableWidget(20, 1, self)
        self.rollTable.setHorizontalHeaderLabels(["Game"])
        self.rollTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rollTable.setStyleSheet(setColorofTableCorner())

        # Card Draw Table
        self.cardTable = QTableWidget(14, 2, self)
        self.cardTable.setHorizontalHeaderLabels(["Card", "Game"])
        self.cardTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.cardTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cardTable.setStyleSheet(setColorofTableCorner())

        # load the card names for the card-draw table
        for i in range(14):
            rowName = QTableWidgetItem(f"{cardDeckNames[i]}")
            rowName.setFlags(rowName.flags() & Qt.ItemIsEditable)
            rowName.setForeground(QColor(Qt.black))
            self.cardTable.setItem(i, 0, rowName)

        # Personal Preference Table + Button
        self.personalTable = QTableWidget(12, 1, self)
        self.personalTable.setHorizontalHeaderLabels(["Game"])
        self.personalTable.setColumnWidth(0, 275)
        self.personalTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.personalTable.setStyleSheet(setColorofTableCorner())

        self.loadPersonalList()

        # I just decided to create the edit window here because it correlates with the personal preference table only
        self.editPersonalTableButton = QPushButton("Edit Want-To-Continue-Playing List")

        self.editPersonalGameListWindow = EditPersonalGameListWindow()
        self.editPersonalGameListWindow.setObjectName("editGamesListWindow")

        self.editPersonalTableButton.clicked.connect(self.showEditPersonalGamesWindow)

        # add widgets to table layout
        self.tableLayout.addWidget(self.rollTable)
        self.tableLayout.addWidget(self.cardTable)

        self.personalTableLayout.addWidget(self.personalTable)
        self.personalTableLayout.addWidget(self.editPersonalTableButton)

        # __BUTTON LAYOUT__

        self.rerollTables = QPushButton("Reroll Tables")
        self.saveTables = QPushButton("Save Table Info")

        # connect buttons
        self.rerollTables.clicked.connect(self.generateTableContents)

        # add widgets to button layout
        self.buttonLayout.addWidget(self.rerollTables)
        self.buttonLayout.addWidget(self.saveTables)

        # add child layouts to main layout
        self.tableLayout.addLayout(self.personalTableLayout)
        self.mainLayout.addLayout(self.tableLayout)
        self.mainLayout.addLayout(self.buttonLayout)

        if detectIfEnoughTimeHasPassed() is True:
            self.generateTableContents()
            self.saveAllInformation()
        else:
            self.loadStoredTables(loadSpecificList("rollGameList"), loadSpecificList("cardDrawList"))
            print("Data load successful")
            printNumberOfDaysLeft()

        # table refresh signal
        self.editPersonalGameListWindow.personalListChangeSignal.connect(self.refreshWindow)

        # set main layout
        self.setLayout(self.mainLayout)

    def showEditPersonalGamesWindow(self):
        self.personalGamesButtonSignal.emit()

    def loadStoredTables(self, diceList, cardList):

        for i in range(20):
            item = QTableWidgetItem(diceList[i])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.rollTable.setItem(i, 0, item)

        for i in range(14):
            item = QTableWidgetItem(cardList[i])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.cardTable.setItem(i, 1, item)

    def generateTableContents(self):
        self.diceRollList.clear()
        self.cardDrawList.clear()
        fullGameList = loadSortedList()

        # dice roll list

        while len(self.diceRollList) < 19:
            randomGame = random.choice(fullGameList)

            if randomGame["completed"] == "Complete":
                randomNum = random.randint(1, 4)
                gameReplayValue = replayabilityStatusReference[randomGame["replayabilityFactor"]]
                if gameReplayValue > randomNum:
                    self.diceRollList.append(randomGame["id"])
                else:
                    continue
            else:
                self.diceRollList.append(randomGame["id"])

        convertGameIDListIntoNames(self.diceRollList)

        for i in range(20):
            item = QTableWidgetItem(self.diceRollList[i])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.rollTable.setItem(i, 0, item)

        # card draw list

        while len(self.cardDrawList) < 13:
            randomGame = random.choice(fullGameList)

            if randomGame["id"] in self.cardDrawList or randomGame["id"] == -1:
                continue
            if randomGame["completed"] == "Complete":
                randomNum = random.randint(1, 4)
                gameReplayValue = replayabilityStatusReference[randomGame["replayabilityFactor"]]
                if gameReplayValue < randomNum:
                    continue

            self.cardDrawList.append(randomGame["id"])

        convertGameIDListIntoNames(self.cardDrawList)

        for i in range(14):
            item = QTableWidgetItem(self.cardDrawList[i])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.cardTable.setItem(i, 1, item)

    def loadPersonalList(self):
        data = loadJSONData()
        loadedPersonalList = data['personalGameList']

        for i in range(len(loadedPersonalList)):
            item = QTableWidgetItem(loadedPersonalList[i])
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            item.setForeground((QColor(Qt.black)))
            self.personalTable.setItem(i, 0, item)

    def saveAllInformation(self):
        data = loadJSONData()

        savedRollTable = data['rollGameList']
        savedDrawTable = data['cardDrawList']

        savedRollTable.clear()
        savedDrawTable.clear()

        data["gameOfTheWeek"] = random.choice(loadSortedList())['name']

        for row in range(20):
            savedRollTable.append(self.rollTable.item(row, 0).text())

        for row in range(14):
            savedDrawTable.append(self.cardTable.item(row, 1).text())

        updateJSONData(data)
        print("Information re-roll successful")
        replaceDate()
        print("Date Replacement successful")

    def refreshWindow(self, confirmation):
        if confirmation:
            self.loadPersonalList()

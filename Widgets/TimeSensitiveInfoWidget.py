from common import *


class TimeSensitiveInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.gameOfTheWeek = ''

        self.mainLayout = QHBoxLayout()

        self.gameOfTheWeekLabel = QLabel()
        self.dailyListLabel = QLabel()

        self.gameOfTheWeekLabel.setAlignment(Qt.AlignCenter)
        self.dailyListLabel.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.gameOfTheWeekLabel)
        self.mainLayout.addWidget(self.dailyListLabel)
        self.setLayout(self.mainLayout)

        if detectIfEnoughTimeHasPassed() is True:
            self.setGameOfTheWeek()
            self.generateNewListSelection()

        else:
            self.loadGameOfTheWeek()
            self.getSelectedList()


    def loadGameOfTheWeek(self):
        with open('ApplicationInformation.json', 'r') as file:
            data = json.load(file)
            loadedGameID = data["gameOfTheWeek"]

            for game in loadSortedList():
                if game["id"] == loadedGameID:
                    self.gameOfTheWeek = game["name"]
                    logProcess(f"Loaded weekly game ({self.gameOfTheWeek})")

            self.gameOfTheWeekLabel.setText(f"__Game of the week__\n\n{self.gameOfTheWeek}")

    def setGameOfTheWeek(self):
        self.gameOfTheWeek = random.choice(loadSortedList())["name"]

        self.gameOfTheWeekLabel.clear()
        self.gameOfTheWeekLabel.setText(f"__Game of the week__\n\n{self.gameOfTheWeek}")
        logProcess(f"New temporary weekly game: ({self.gameOfTheWeek})")

    def getSelectedList(self):
        with open('ApplicationInformation.json', 'r') as file:
            data = json.load(file)
            weeklyListSelection = data["weeklyListSelection"]
        day = datetime.today().weekday()
        self.dailyListLabel.setText(f"__Daily List__\n\n{weeklyListSelection[day]}")

    def generateNewListSelection(self):
        # load the weekly list and clear it
        data = loadJSONData()
        weeklyListSelection = data['weeklyListSelection']
        weeklyListSelection.clear()
        # shuffle the base selection pool
        random.shuffle(weeklySelectionPool)
        weeklyListSelection = weeklySelectionPool

        data['weeklyListSelection'] = weeklyListSelection
        updateJSONData(data)

    def saveGameOfTheWeek(self):
        print(self.gameOfTheWeek)
        data = loadJSONData()
        data["gameOfTheWeek"] = getIdByName(self.gameOfTheWeek)
        print(data["gameOfTheWeek"])
        updateJSONData(data)
        logProcess(f"New Game of The Week: {searchGameByID(loadJSONData()['gameOfTheWeek'])['name']}")


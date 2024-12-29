from common import *


class TimeSensitiveInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):

        # GUI variables
        self.mainLayout = QHBoxLayout()

        self.gameOfTheWeekLabel = QLabel()
        self.dailyListLabel = QLabel()

        self.gameOfTheWeekLabel.setAlignment(Qt.AlignCenter)
        self.dailyListLabel.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.gameOfTheWeekLabel)
        self.mainLayout.addWidget(self.dailyListLabel)
        self.setLayout(self.mainLayout)

        # Class variables
        self.currentGameOfTheWeekID = ''
    def loadGameOfTheWeek(self):
        with open('ApplicationInformation.json', 'r') as file:
            data = json.load(file)
            loadedGameID = data["gameOfTheWeek"]
            print(loadedGameID)

            for game in loadSortedList():
                if game["id"] == loadedGameID:
                    gameOfWeek = game["name"]
                    logProcess(f"Loaded weekly game ({gameOfWeek})")

            self.gameOfTheWeekLabel.setText(f"__Game of the week__\n\n{loadGameOfTheWeek()}")

    def setGameOfTheWeekLabel(self):
        self.gameOfTheWeekLabel.clear()
        self.gameOfTheWeekLabel.setText(f"__Game of the week__\n\n{loadGameOfTheWeek()}")


    # this creates a temporary game of the week when the app contents are rerolled manually
    def createTempWeeklyGame(self):
        data = loadJSONData()
        tempWeeklyGameSelection = random.choice(data["fullGameList"])
        self.gameOfTheWeekLabel.setText(f"__Game of the week__\n\n{tempWeeklyGameSelection['name']}")
        self.currentGameOfTheWeekID = tempWeeklyGameSelection['id']
        print(f'Current Game of the Week ID: {self.currentGameOfTheWeekID}')


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
        print(f"Previous list selection: {weeklyListSelection}")
        weeklyListSelection.clear()
        # shuffle the base selection pool
        weeklyListSelection = sorted(weeklySelectionPool, key=lambda x: random.random())
        print(f"New list selection: {weeklyListSelection}")
        data['weeklyListSelection'] = weeklyListSelection
        updateJSONData(data)


    def weeklyUpdate(self, timePassedConditional):
        if timePassedConditional:
            self.setGameOfTheWeekLabel()
            self.generateNewListSelection()
            self.getSelectedList()
        else:
            self.loadGameOfTheWeek()
            self.getSelectedList()
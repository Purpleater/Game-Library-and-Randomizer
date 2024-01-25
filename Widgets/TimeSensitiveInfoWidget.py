

from common import *


class TimeSensitiveInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
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

        else:
            self.loadGameOfTheWeek()
            self.getSelectedList()


    def loadGameOfTheWeek(self):
        with open('ApplicationInformation.json', 'r') as file:
            data = json.load(file)
            gameOfTheWeek = data["gameOfTheWeek"]
            self.gameOfTheWeekLabel.setText(f"__Game of the week__\n{gameOfTheWeek}")

    def setGameOfTheWeek(self):
        gameOfTheWeek = random.choice(loadSortedList())["name"]
        self.gameOfTheWeekLabel.clear()
        self.gameOfTheWeekLabel.setText(f"__Game of the week__\n{gameOfTheWeek}")

    def getSelectedList(self):
        with open('ApplicationInformation.json', 'r') as file:
            data = json.load(file)
            weeklyListSelection = data["weeklyListSelection"]
        day = datetime.today().weekday()
        self.dailyListLabel.setText(f"__Daily List__\n{weeklyListSelection[day]}")



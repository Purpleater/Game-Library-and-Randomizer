from common import *
from PyQt5.QtCore import pyqtSignal


class EditPersonalGameListWindow(QWidget):
    # this notifies the tables widget to refresh itself whenever the list is adjusted
    pListChangeSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widgetUI()
        selectedGame = ''

    def widgetUI(self):
        # initialize main layout
        self.mainLayout = QStackedLayout()

        # import child menus into class
        self.swapOutMenu = SwapOutMenu()
        self.swapInMenu = SwapInMenu()

        # stack 'em
        self.mainLayout.addWidget(self.swapOutMenu)
        self.mainLayout.addWidget(self.swapInMenu)

        # set connection slots
        self.swapOutMenu.continueSignal.connect(self.showSwapInMenu)
        self.swapOutMenu.selectedGameSignal.connect(self.getSelectedGame)
        self.swapInMenu.backSignal.connect(self.showSwapOutMenu)
        self.swapInMenu.updatePersonalListSignal.connect(self.updatePersonalList)
        self.swapInMenu.closeWindowRequestSignal.connect(self.hide)

        # set the main layout as, well, the main layout
        self.setLayout(self.mainLayout)
        self.mainLayout.setCurrentIndex(0)

    def showSwapOutMenu(self):
        self.mainLayout.setCurrentIndex(0)

    def showSwapInMenu(self):
        self.mainLayout.setCurrentIndex(1)

    def getSelectedGame(self, game):
        self.swapInMenu.getSelectedGame(game)

    def updatePersonalList(self):
        self.pListChangeSignal.emit()
        logProcess("Personal Tables table refresh signal relayed to main widget")

    def hideWindow(self):
        self.hide()


class SwapOutMenu(QWidget):
    continueSignal = pyqtSignal()
    selectedGameSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.selectedGame = ''

        # layouts
        self.mainLayout = QVBoxLayout()

        # widgets
        self.instructionLabel = QLabel("Please select the game you would like to replace: ")
        self.selectionList = QListWidget()
        self.submissionButton = QPushButton("Submit Game")

        # connect button
        self.submissionButton.clicked.connect(self.emitSignalToContinue)

        # add stuff to layouts
        self.mainLayout.addWidget(self.instructionLabel)
        self.mainLayout.addWidget(self.selectionList)
        self.mainLayout.addWidget(self.submissionButton)

        self.setLayout(self.mainLayout)
        self.populateList()

    def populateList(self):
        self.selectionList.clear()
        for game in loadPersonalList():
            self.selectionList.addItem(searchGameByID(game)["name"])

    def emitSignalToContinue(self):
        self.continueSignal.emit()
        self.selectedGameSignal.emit(getIdByName(self.selectionList.selectedItems()[0].text()))


class SwapInMenu(QWidget):
    backSignal = pyqtSignal()
    updatePersonalListSignal = pyqtSignal()
    closeWindowRequestSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.selectedSwapOutGame = ''

        # layouts
        self.mainLayout = QVBoxLayout()
        self.listSearchLayout = QHBoxLayout()
        self.buttonRowLayout = QHBoxLayout()

        # widgets
        self.findGameLabel = QLabel("Search For a Game")
        self.instructionLabel = QLabel("Please select the game you would like to add to the list: ")
        self.listSearch = QLineEdit()
        self.selectionList = QListWidget()
        self.submissionButton = QPushButton("Submit Game")
        self.backButton = QPushButton("Back")

        # connections
        self.listSearch.textChanged.connect(self.updateSearchList)
        self.backButton.clicked.connect(self.returnToPreviousPage)
        self.submissionButton.clicked.connect(self.submitGame)
        # add stuff to layouts
        self.listSearchLayout.addWidget(self.findGameLabel)
        self.listSearchLayout.addWidget(self.listSearch)

        self.buttonRowLayout.addWidget(self.backButton)
        self.buttonRowLayout.addWidget(self.submissionButton)

        # add child layouts to the parent
        self.mainLayout.addWidget(self.instructionLabel)
        self.mainLayout.addLayout(self.listSearchLayout)
        self.mainLayout.addWidget(self.selectionList)
        self.mainLayout.addLayout(self.buttonRowLayout)

        self.setLayout(self.mainLayout)

    # this method is used to set the corresponding value from the SwapInMenu class
    def getSelectedGame(self, game):
        self.selectedSwapOutGame = game
        logProcess(f"Selected ({searchGameByID(game)['name']}) to swap out of list")
        self.loadFilteredList()

    def returnToPreviousPage(self):
        self.backSignal.emit()
        self.listSearch.clear()

    def loadFilteredList(self):
        personalList = loadPersonalList()
        self.selectionList.clear()
        for game in loadSortedList():
            filteredGame = False
            if game['id'] == self.selectedSwapOutGame:
                filteredGame = True
            if game['id'] in personalList:
                filteredGame = True
            if not filteredGame:
                self.selectionList.addItem(game["name"])

    def updateSearchList(self):
        searchValue = self.listSearch.text().lower()
        self.selectionList.clear()
        for game in loadSortedList():
            if game["id"] == self.selectedSwapOutGame or game["id"] in loadPersonalList():
                continue
            else:
                if searchValue in game["name"].lower():
                    self.selectionList.addItem(game["name"])

    def styleInputField(self, palette):
        self.listSearch.setStyleSheet(setColorForInputLines(palette))

    def submitGame(self):
        selectedSwapInGame = getIdByName(self.selectionList.selectedItems()[0].text())
        selectedGames = [self.selectedSwapOutGame, selectedSwapInGame]

        gameSwapConfirmation = self.showGameEditConfirmationWindow(selectedGames)
        print(gameSwapConfirmation)
        if gameSwapConfirmation:
            list = loadPersonalList()
            for i in range(len(list)):
                if list[i] == selectedGames[0]:
                    list[i] = selectedGames[1]

        # save the updated list
        data = loadJSONData()
        personalList = data['personalGameList']
        for i in range(len(personalList)):
            personalList[i] = list[i]
        updateJSONData(data)

        # ping main window
        self.updatePersonalList()

        # prompt the user to close the window
        if self.closeWindowRequest():
            self.closeWindowRequestSignal.emit()

    def updatePersonalList(self):
        self.updatePersonalListSignal.emit()

    def showGameEditConfirmationWindow(self, selectedGames):
        processText = f"Would you like to swap [{searchGameByID(selectedGames[0])['name']}] for [{searchGameByID(selectedGames[1])['name']}]?"
        trueArrayList = [windowLogProcess(f"[{searchGameByID(selectedGames[0])['name']}] swapped for [{searchGameByID(selectedGames[1])['name']}] in personal games list")]
        falseArrayList = [windowLogProcess(f"Cancelled a game swap in the personal list")]
        return createStandardConfirmationWindow(processText, "Swap Confirmation", trueArrayList, falseArrayList)

    def closeWindowRequest(self):
        processText = f"Game swap was successful, would you like to close the window?"
        trueArrayList = [windowLogProcess("Game Swap Successful"), self.returnToPreviousPage, self.closeWindowRequestSignal.emit, self.updatePersonalList]
        createStandardConfirmationWindow(processText, "Game Swap Successful", trueArrayList, [])



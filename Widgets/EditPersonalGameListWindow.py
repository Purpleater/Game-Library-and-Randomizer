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

        # set the main layout as, well, the main layout
        self.setLayout(self.mainLayout)
        self.mainLayout.setCurrentIndex(0)

    def showSwapOutMenu(self):
        self.mainLayout.setCurrentIndex(0)

    def showSwapInMenu(self):
        self.mainLayout.setCurrentIndex(1)

    def getSelectedGame(self, game):
        self.swapInMenu.getSelectedGame(game)


class SwapOutMenu(QWidget):
    continueSignal = pyqtSignal()
    selectedGameSignal = pyqtSignal(str)
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
            self.selectionList.addItem(game)


    def emitSignalToContinue(self):
        self.continueSignal.emit()
        self.selectedGameSignal.emit(self.selectionList.selectedItems()[0].text())

class SwapInMenu(QWidget):
    backSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.selectedGame = ''

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
        self.loadFilteredList()

    # this method is used to set the corresponding value from the SwapInMenu class
    def getSelectedGame(self, game):
        self.selectedSwapOutGame = game
        logProcess(f"Selected ({game}) to swap out of list")

    def returnToPreviousPage(self):
        self.backSignal.emit()
        self.listSearch.clear()
        self.loadFilteredList()


    def loadFilteredList(self):
        self.selectionList.clear()
        for game in loadSortedList():
            if game["name"] != game and game["name"] not in loadPersonalList():
                self.selectionList.addItem(game["name"])

    def updateSearchList(self):
        searchValue = self.listSearch.text().lower()
        self.selectionList.clear()
        for game in loadSortedList():
            if game["name"] == self.selectedSwapOutGame or game["name"] in loadPersonalList():
                continue
            else:
                if searchValue in game["name"].lower():
                    self.selectionList.addItem(game["name"])

    def submitGame(self):
        selectedSwapInGame = self.selectionList.selectedItems()[0].text()
        selectedGames = [self.selectedSwapOutGame, selectedSwapInGame]

        gameSwapConfirmation = self.showGameEditConfirmationWindow(selectedGames)
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

        # prompt the user to close the window
        closeWindowRequest("Game swap", self)

    def showGameEditConfirmationWindow(self, selectedGames):

        editGameConfirmationWindow = QMessageBox()
        editGameConfirmationWindow.setText(f"Would you like to swap [{selectedGames[0]}] for [{selectedGames[1]}]?")
        editGameConfirmationWindow.setWindowTitle("Edit Game Confirmation")
        editGameConfirmationWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = editGameConfirmationWindow.exec_()

        if returnValue == QMessageBox.Yes:
            logProcess(f"[{selectedGames[0]}] swapped for [{selectedGames[1]}] in personal games list")
            return True
        if returnValue == QMessageBox.No:
            logProcess(f"Cancelled a game swap in the personal list")
            return False

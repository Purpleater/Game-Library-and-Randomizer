from common import *
from PyQt5.QtCore import pyqtSignal

class EditPersonalGameListWindow(QWidget):
    # this notifies the tables widget to refresh itself whenever the list is adjusted
    personalListChangeSignal = pyqtSignal(bool)


    def __init__(self):
        super().__init__()
        self.widgetUI()


    def widgetUI(self):

        self.clickCount = 1
        self.selectedGames = []

        self.mainLayout = QVBoxLayout()
        self.listSearchLayout = QHBoxLayout()
        self.buttonRowLayout = QHBoxLayout()

        self.instructionLabel = QLabel("Please select the game you would like to replace: ")
        self.findGameLabel = QLabel("Search For a Game")
        self.listSearch = QLineEdit()
        self.selectionList = QListWidget()

        self.submissionButton = QPushButton("Submit Game")
        self.submissionButton.clicked.connect(self.selectGameToReplace)
        print(self.submissionButton.palette())

        self.goBackButton = QPushButton("Back")
        self.goBackButton.clicked.connect(self.returnToPreviousPage)

        # add widgets to list search layout
        self.listSearchLayout.addWidget(self.findGameLabel)
        self.listSearchLayout.addWidget(self.listSearch)
        self.listSearch.textChanged.connect(self.updateList)

        self.findGameLabel.hide()
        self.listSearch.hide()

        # add stuff to child layouts
        self.buttonRowLayout.addWidget(self.goBackButton)
        self.buttonRowLayout.addWidget(self.submissionButton)

        self.goBackButton.hide()

        self.mainLayout.addWidget(self.instructionLabel)
        self.mainLayout.addLayout(self.listSearchLayout)
        self.mainLayout.addWidget(self.selectionList)
        self.mainLayout.addLayout(self.buttonRowLayout)

        # connect the list search widget to the correct method
        self.listSearch.textChanged.connect(self.updateList)
        self.populateList()

        # set the stylesheet because I can't do that in main apparently
        self.setColorPalette()
        # set main layout
        self.setLayout(self.mainLayout)

    def populateList(self):
        self.selectionList.clear()
        for game in loadPersonalList():
            self.selectionList.addItem(game)

    def selectGameToReplace(self):

        if self.clickCount == 1:
            selectedGame = self.selectionList.selectedItems()[0].text()
            self.selectedGames.append(selectedGame)
            self.selectionList.clear()

            # reveal hidden input field and label
            self.findGameLabel.show()
            self.listSearch.show()
            self.goBackButton.show()

            self.instructionLabel.setText("Please select the game you would like to add to the list: ")
            for game in loadSortedList():
                if game["name"] != selectedGame and game["name"] not in loadPersonalList():
                    self.selectionList.addItem(game["name"])
            self.clickCount += 1


        elif self.clickCount == 2:
            selectedGame = self.selectionList.selectedItems()[0].text()
            self.selectedGames.append(selectedGame)

            # convert user's confirmation into a value that can be evaluated by both the signal and the conditional
            gameEditConfirmationValue = self.showGameEditConfirmationWindow(self.selectedGames)
            if gameEditConfirmationValue:
                list = loadPersonalList()
                for i in range(len(list)):
                    if list[i] == self.selectedGames[0]:
                        list[i] = self.selectedGames[1]

                # save the updated list
                data = loadJSONData()
                personalList = data['personalGameList']
                for i in range(len(personalList)):
                    personalList[i] = list[i]
                updateJSONData(data)
                showProcessConfirmationWindow("Game swap")
                self.listChangeConfirmationPing(gameEditConfirmationValue)
                self.populateList()

            self.selectionList.clear()
            self.populateList()
            self.instructionLabel.setText("Please select the game you would like to replace: ")
            self.selectedGames.clear()
            self.clickCount = 1

    def showGameEditConfirmationWindow(self, selectedGames):

        editGameConfirmationWindow = QMessageBox()
        editGameConfirmationWindow.setText(f"Would you like to swap [{selectedGames[0]}] for [{selectedGames[1]}]?")
        editGameConfirmationWindow.setWindowTitle("Edit Game Confirmation")
        editGameConfirmationWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = editGameConfirmationWindow.exec_()

        if returnValue == QMessageBox.Yes:
            return True
        if returnValue == QMessageBox.No:
            return False

    def updateList(self):
        self.selectionList.clear()
        for game in loadSortedList():
            if self.listSearch.text().lower() in game["name"].lower():
                self.selectionList.addItem(game["name"])

    def listChangeConfirmationPing(self, confirmationBool):
        if confirmationBool:
            self.personalListChangeSignal.emit(True)

    def returnToPreviousPage(self):
        self.instructionLabel.setText("Please select the game you would like to replace: ")
        self.clickCount = 1
        self.selectionList.clear()
        self.populateList()
        self.goBackButton.hide()
        self.listSearch.hide()
        self.findGameLabel.hide()

    def setColorPalette(self):
        data = loadJSONData()
        colorPalette = data["savedColorPalette"]
        with open(f'Color Palettes/{colorPalette}.css') as stylesheet:
            style = stylesheet.read()
        self.setStyleSheet(style)


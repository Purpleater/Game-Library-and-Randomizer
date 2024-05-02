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

        # set the main layout as, well, the main layout
        self.setLayout(self.mainLayout)
        self.mainLayout.setCurrentIndex(0)

    def showSwapOutMenu(self):
        printMeese()

    def showSwapInMenu(self):
        self.mainLayout.setCurrentIndex(1)


class SwapOutMenu(QWidget):
    continueSignal = pyqtSignal()
    selectedGameSignal = pyqtSignal()
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
        self.selectedGameSignal.emit()

class SwapInMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.selectedSwapOutGame = ''

        # initialize SwapOutMenu :eyeroll:
        self.swapOutMenu = SwapOutMenu()

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

        # set connection slots

        self.swapOutMenu.selectedGameSignal.connect(printMeese)

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


'''
    def loadFilteredList(self):
        print(EditPersonalGameListWindow.returnSelectedGame())
        for game in loadSortedList():
            if game["name"] != game and game["name"] not in loadPersonalList():
                self.selectionList.addItem(game["name"])
'''



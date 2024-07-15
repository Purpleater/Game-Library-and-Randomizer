import sys
import random
from PyQt5.QtWidgets import *
import json
from json import JSONEncoder
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QColor
from datetime import *
import os
import shutil


completionStatusReference = {
    "Incomplete": 0,
    "Complete": 1,
    "No Ending": 2
}
replayabilityStatusReference = {
    "Low": 0,
    "Moderate": 1,
    "High": 2,
    "Very High": 3
}

cardDeckNames = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King",
                 "Joker"]

weeklySelectionPool = ["Roll", "Roll", "Card Draw", "Card Draw", "Want To Continue Playing", "Want To Continue Playing",
                       "Free Day"]
currentlyAppliedColorScheme = ""

class Game:
    def __init__(self, name, completed, replayabilityFactor):
        self.name = name
        self.completed = completed
        self.replayabilityFactor = replayabilityFactor

    def toJSON(self):
        gameId = getLastGameId()
        updateLastGameID()
        return {
            'name': self.name,
            'id': gameId,
            'completed': self.completed,
            'replayabilityFactor': self.replayabilityFactor
        }


def loadJSONData():
    with open('ApplicationInformation.json', 'r') as file:
        data = json.load(file)
        return data


def updateJSONData(data):
    with open('ApplicationInformation.json', 'w') as file:
        json.dump(data, file, indent=4)


def getLastGameId():
    data = loadJSONData()
    lastUsedId = int(data["lastGameId"])
    return lastUsedId


def updateLastGameID():
    data = loadJSONData()
    lastId = int(data["lastGameId"])
    data["lastGameId"] = lastId + 1
    updateJSONData(data)


def updateFullGameList(newGame):
    data = loadJSONData()
    fullGameList = data['fullGameList']
    fullGameList.append(newGame)
    updateJSONData(data)


def getNumberOfPointsFromFile():
    data = loadJSONData()
    pointsNumber = data["numberOfPoints"]
    return pointsNumber


def loadSortedList():
    data = loadJSONData()
    listOfGames = data['fullGameList']
    sortedGameList = sorted(listOfGames, key=lambda x: x["name"])
    return sortedGameList


def loadPersonalList():
    data = loadJSONData()
    personalList = data['personalGameList']
    return personalList


def findDictionaryKey(dictionary, item):
    for key, value in dictionary.items():
        if value == item:
            return key


# this is here because there's tons of processes that I want to confirm are working lmao
def showProcessConfirmationWindow(specificProcess):
    def processConfirmation():
        processConfirmationWindow = QMessageBox()
        processConfirmationWindow.setText(f"{specificProcess} was successful!")
        processConfirmationWindow.setWindowTitle("Success")

        returnValue = processConfirmationWindow.exec_()

    return processConfirmation()


def editExistingGameInformation(gameId, gameName, gameCompletion, gameReplayability):
    data = loadJSONData()

    for game in data['fullGameList']:
        if game["id"] == gameId:
            game["name"] = gameName
            game["completed"] = gameCompletion
            game["replayabilityFactor"] = gameReplayability
            logProcess(f"Updated Entry: {game}")

    updateJSONData(data)


def detectIfEnoughTimeHasPassed():
    todaysDate = datetime.now()
    data = loadJSONData()
    savedDate = data['savedDate']
    dateObject = datetime.strptime(savedDate, "%Y,%m,%d")
    daysDifference = (todaysDate - dateObject).days

    if daysDifference > 6:
        return True
    else:
        return False


def printNumberOfDaysLeft():
    todaysDate = datetime.now()
    data = loadJSONData()
    savedDate = data['savedDate']
    dateObject = datetime.strptime(savedDate, "%Y,%m,%d")
    daysDifference = daysDifference = (todaysDate - dateObject).days
    print(f"Number of Days left before next re-roll: {7 - daysDifference}")


def loadSpecificList(listName):
    data = loadJSONData()
    list = data[listName]
    return list


def replaceDate():
    data = loadJSONData()
    todaysDate = datetime.now()
    newDate = todaysDate.strftime("%Y,%m,%d")
    data["savedDate"] = newDate
    updateJSONData(data)


def loadColorPallet():
    data = loadJSONData()
    colorPalette = data["savedColorPalette"]
    return colorPalette


def setStyle(widget, colorPalette):
    with open(f'Color Palettes/{colorPalette}.css') as stylesheet:
        style = stylesheet.read()
    widget.setStyleSheet(style)
    print(f'Applied ({colorPalette}) style to: {widget}')


def setColorPalletForComboBox(palette):
    # idk why but I started at the bottom for all manual styling and then went up from there
    # whatever
    # [0] for the border color
    # [1] for textColor
    # [2] for the font weight of the combo box

    paletteList = loadJSONData()["colorPaletteList"]
    stylingList = []
    for item in paletteList:
        if palette == item["file"]:
            stylingList = item["comboBoxStyling"]
    borderColor = stylingList[0]
    textColor = stylingList[1]
    fontWeight = stylingList[2]

    return f"QComboBox {{ border: 1px solid {borderColor}; color: {textColor}; {fontWeight};}}"


def setColorofTableCorner(palette):
    paletteList = loadJSONData()["colorPaletteList"]
    cornerColor = ''
    for item in paletteList:
        if palette == item["file"]:
            cornerColor = item["tableCornerColor"]

    return f"QTableView QTableCornerButton::section{{ background: {cornerColor}; }}"


def setColorForInputLines(palette):
    # drawing from colorPaletteList in ApplicationInformation.json
    # more specifically the inputLineStyling array, which stores the hexcode values
    # [0] in the array is the inputLine Coloring
    # [1] is the border color

    paletteList = loadJSONData()["colorPaletteList"]
    stylingList = []
    for item in paletteList:
        if palette == item["file"]:
            stylingList = item["inputLineStyling"]

    inputTextStylingColor = stylingList[0]
    inputBorderColor = stylingList[1]

    styling = (
        f"QLineEdit{{color:{inputTextStylingColor}; border: 2px solid {inputBorderColor}}}"
        f"QLineEdit:focus{{color:{inputTextStylingColor};}}"
    )
    return styling

# one of these is for standard processes
# and the other is specifically for confirmation display windows
# I wish it wasn't this way but this is the reality we live in

def logProcess(process):
    currentTime = datetime.now().strftime('%H:%M:%S')
    print(f'{currentTime} - {process}')

def windowLogProcess(process):
    def log():
        currentTime = datetime.now().strftime('%H:%M:%S')
        print(f'{currentTime} - {process}')

    return log

def createStandardConfirmationWindow(textString, windowTitle, trueProcessArray, falseProcessArray):
    standardConfirmationWindow = QMessageBox()
    standardConfirmationWindow.setText(textString)
    standardConfirmationWindow.setWindowTitle(windowTitle)
    standardConfirmationWindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    returnValue = standardConfirmationWindow.exec_()

    if returnValue == QMessageBox.Yes:
        if len(trueProcessArray) != 0:
            for process in trueProcessArray:
                process()
        return True
    if returnValue == QMessageBox.No:
        if len(falseProcessArray) != 0:
            for process in falseProcessArray:
                process()
        return False


def closeWindowRequest(process, window):
    processString = f"{process} successful, would you like to close this window?"
    createStandardConfirmationWindow(processString, "Process Successful", [window.hide], [])


def searchGameByID(gameID):
    if gameID == -1:
        return {"name": "Free Choice", "id": -1}
    for game in loadSortedList():
        if gameID == game['id']:
            return game


def getIdByName(gameName):
    for game in loadSortedList():
        if gameName == game["name"]:
            return game["id"]


def checkForPreexistingFile(directory, newFile):
    directoryFiles = os.listdir(directory)
    if newFile in directoryFiles:
        logProcess("Duplicate styling file detected")
        return True


# this is just a debug method
def printMeese():
    print("Meese")

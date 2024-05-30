import sys
import random
from PyQt5.QtWidgets import *
import json
from json import JSONEncoder
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QColor
from datetime import *
from PyQt5.QtCore import pyqtSignal

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


def setColorPalletForComboBox(colorPalette):
    borderColorDictionary = {
        "contrast": "white",
        "sunset": "#985277",
        "black-space": "#D4D4D4",
        "strange-waters": "#296647",
    }
    textColorDictionary = {
        "contrast": "white",
        "sunset": "#5c374c",
        "black-space": "#D4D4D4",
        "strange-waters": "#23AD8F",

    }
    fontWeight = {
        "contrast": "",
        "sunset": "font-weight: bold;",
        "black-space": "",
        "strange-waters": "",
    }
    editableTextColor = {
        "contrast": "white",
        "sunset": "#5c374c",
        "black-space": "yellow",
        "strange-waters": "#296647",

    }
    borderColor = borderColorDictionary[colorPalette]
    return f"QComboBox {{ border: 1px solid {borderColor}; color: {textColorDictionary[colorPalette]}; {fontWeight[colorPalette]};}}"


def setColorofTableCorner(palette):
    cornerColorDictionary = {
        "contrast": "black",
        "sunset": "#ff8c61",
        "black-space": "#c79c00",
        "strange-waters": "#173535",
    }
    return f"QTableView QTableCornerButton::section{{ background: {cornerColorDictionary[palette]}; }}"


def setColorForInputLines(palette):
    inputLineDictionary = {
        "contrast": "white",
        "sunset": "#5c374c",
        "black-space": "yellow",
        "strange-waters": "#23AD8F",

    }
    fontWeight = {
        "contrast": "",
        "sunset": "font-weight: bold;",
        "black-space": "yellow",
        "strange-waters": "",
    }

    inputBorderColor = {
        "contrast": "white",
        "sunset": "#985277",
        "black-space": "white",
        "strange-waters": "#23AD8F"
    }

    styling = (
        f"QLineEdit{{color:{inputLineDictionary[palette]}; border: 2px solid {inputBorderColor[palette]}}}"
        f"QLineEdit:focus{{color:{inputLineDictionary[palette]};}}"
    )
    return styling


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


# this is just a debug method
def printMeese():
    print("Meese")

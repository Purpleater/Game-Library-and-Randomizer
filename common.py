import sys
import random
from PyQt5.QtWidgets import *
import json
from json import JSONEncoder
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from datetime import *

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


def getLastGameId():
    with open('ApplicationInformation.json', 'r') as file:
        data = json.load(file)
        lastUsedId = int(data["lastGameId"])
    return lastUsedId


def updateLastGameID():
    with open('ApplicationInformation.json', 'r') as file:
        data = json.load(file)
        lastId = int(data["lastGameId"])
        data["lastGameId"] = lastId + 1

    with open('ApplicationInformation.json', 'w') as file:
        json.dump(data, file, indent=4)


def updateFullGameList(newGame):
    with open('ApplicationInformation.json', 'r') as file:
        data = json.load(file)
        fullGameList = data['fullGameList']
        fullGameList.append(newGame)
    with open('ApplicationInformation.json', 'w') as file:
        json.dump(data, file, indent=4)


def getNumberOfPointsFromFile():
    with open('ApplicationInformation.json', 'r') as file:
        data = json.load(file)
        pointsNumber = data["numberOfPoints"]
    return pointsNumber


def loadSortedList():
    with open('ApplicationInformation.json', 'r') as file:
        data = json.load(file)
        listOfGames = data['fullGameList']
        sortedGameList = sorted(listOfGames, key=lambda x: x["name"])
    return sortedGameList


def loadPersonalList():
    with open('ApplicationInformation.json', 'r') as file:
        data = json.load(file)
        personalList = data['personalGameList']
    return personalList


def findDictionaryKey(dictionary, item):
    for key, value in dictionary.items():
        if value == item:
            return key


# this is here because there's tons of processes that I want to confirm are working lmao
def showProcessConfirmationWindow(specificProcess):
    processConfirmationWindow = QMessageBox()
    processConfirmationWindow.setText(f"{specificProcess} was successful!")
    processConfirmationWindow.setWindowTitle("Success")

    returnValue = processConfirmationWindow.exec_()


def editExistingGameInformation(gameId, gameCompletion, gameReplayability):
    with open('ApplicationInformation.json', 'r') as file:
        gameListData = json.load(file)

    for game in gameListData['fullGameList']:
        if game["id"] == gameId:
            game["completed"] = gameCompletion
            game["replayabilityFactor"] = gameReplayability
            print(f"Updated Entry: {game}")

    with open('ApplicationInformation.json', 'w') as file:
        json.dump(gameListData, file, indent=4)


def convertGameIDListIntoNames(gameList):
    for i in range(len(gameList)):
        for game in loadSortedList():
            if gameList[i] == game["id"]:
                gameList[i] = game["name"]
    gameList.append("Free Space (Pick Any Game)")

def detectIfEnoughTimeHasPassed():
    todaysDate = datetime.now()
    with open('ApplicationInformation.json', 'r') as file:
        data = json.load(file)
        savedDate = data['savedDate']
    dateObject = datetime.strptime(savedDate, "%Y,%m,%d")
    daysDifference = (todaysDate - dateObject).days

    if daysDifference > 6:
        return True
    else:
        return False

def loadSpecificList(listName):
    with open('ApplicationInformation.json', 'r') as file:
        data = json.load(file)
        list = data[listName]
    return list

def replaceDate():
    with open('ApplicationInformation.json', 'r') as file:
        data = json.load(file)
        todaysDate = datetime.now()
        newDate = todaysDate.strftime("%Y,%m,%d")
        data["savedDate"] = newDate

    with open('ApplicationInformation.json', 'w') as file:
        json.dump(data, file, indent=4)


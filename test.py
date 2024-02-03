from common import *


# this is just a spare file that I use to test out a variety of features

def checkIfGameInPersonalList(string):
    if string in loadPersonalList():
        print("This game is in your personal games list")
    else:
        print("This game is not in your personal games list")

checkIfGameInPersonalList("Dave The Diver")
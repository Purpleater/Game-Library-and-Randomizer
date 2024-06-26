from common import *

from Widgets.CustomPointsValueWindow import CustomPointsValueWidget
from Widgets.EditGamesWindow import EditGameWindow
from Widgets.EditPersonalGameListWindow import EditPersonalGameListWindow
from Widgets.PointsAdjustmentWidget import PointsAdjustmentWidget
from Widgets.TablesWidget import TablesWidget
from Widgets.TimeSensitiveInfoWidget import TimeSensitiveInfoWidget


def setStyle(widget, colorPalette):
    with open(f'Color Palettes/{colorPalette}.css') as stylesheet:
        style = stylesheet.read()
    widget.setStyleSheet(style)


def massApplyStyles(moduleList, colorPalette):
    for item in moduleList:
        setStyle(item, colorPalette)

    logProcess(f"Applied ({colorPalette}) theme to program")


def processTheme(listSelectValue):
    data = loadJSONData()
    themeList = data["colorPaletteList"]
    for palette in themeList:
        if palette["name"] == listSelectValue:
            print(palette["file"])
            return palette["file"]

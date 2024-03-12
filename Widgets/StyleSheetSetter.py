from common import *

from Widgets.ColorModeSelectionWindow import ColorSelectionWindow
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
    print(f'Applied ({colorPalette}) style to: {widget}')


def massApplyStyles(moduleList, colorPalette):
    for item in moduleList:
        setStyle(item, colorPalette)

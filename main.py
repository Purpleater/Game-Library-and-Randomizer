import os
from PyQt5.QtCore import QCoreApplication

import common
from common import *
from Widgets.StyleSheetSetter import *


# import Widgets
from Widgets.TablesWidget import TablesWidget
from Widgets.PointsAdjustmentWidget import PointsAdjustmentWidget
from Widgets.TimeSensitiveInfoWidget import TimeSensitiveInfoWidget
from Widgets.EditGamesWindow import EditGameWindow
from Widgets.CustomPointsValueWindow import CustomPointsValueWidget
from Widgets.EditPersonalGameListWindow import EditPersonalGameListWindow
from Widgets.CustomStyleSheetNamingWindow import CustomStyleSheetNamingWindow
from Widgets.OptionsMenuWindow import OptionsMenu



class MainApplication(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()


    def getWidgetList(self):
        return self.widgetList
    def init_ui(self):
        self.setWindowTitle("Main Application")
        self.setGeometry(100, 100, 1200, 855)

        # create layout
        self.mainLayout = QGridLayout()
        self.informationButtonLayout = QHBoxLayout()
        self.extraSettingsBar = QHBoxLayout()

        # create buttons for extras and settings

        self.editGameListInformationButton = QPushButton("Edit/Add To Game List")
        self.exitButton = QPushButton("Exit Program")
        self.optionsButton = QPushButton("Options")

        # connect buttons to methods
        self.editGameListInformationButton.clicked.connect(self.showGameListWindow)
        self.exitButton.clicked.connect(self.quitApplication)


        # add extra settings buttons to layout

        self.extraSettingsBar.addWidget(self.editGameListInformationButton)
        self.extraSettingsBar.addWidget(self.optionsButton)
        self.extraSettingsBar.addWidget(self.exitButton)


        # initialize the windows within the scope of the main application
        self.tableWidget = TablesWidget()
        self.pointInfoWidget = PointsAdjustmentWidget()
        self.timeSensitiveInfoWidget = TimeSensitiveInfoWidget()
        self.editGameListWindow = EditGameWindow()
        self.customPointsValueWidget = CustomPointsValueWidget()
        self.editPersonalGamesListInfo = EditPersonalGameListWindow()
        self.customStyleSheetNamingWindow = CustomStyleSheetNamingWindow()
        self.optionsMenu = OptionsMenu()


        # set object names for the stylesheet to reference

        self.tableWidget.setObjectName("tableWidget")
        self.pointInfoWidget.setObjectName("pointInfoWidget")
        self.timeSensitiveInfoWidget.setObjectName("timeSensitiveInfoWidget")
        self.editGameListWindow.setObjectName("editGameListWindow")
        self.customPointsValueWidget.setObjectName("customPointsValueWidget")
        self.editPersonalGamesListInfo.setObjectName("editPersonalGamesListInfo")
        self.customStyleSheetNamingWindow.setObjectName("customStyleSheetNamingWindow")
        self.optionsMenu.setObjectName("optionsMenu")

        self.widgetList = [
            self.tableWidget,
            self.pointInfoWidget,
            self.timeSensitiveInfoWidget,
            self.editGameListWindow,
            self.customPointsValueWidget,
            self.editPersonalGamesListInfo,
            self.optionsMenu
        ]

        # color selected signal
        self.optionsMenu.colorThemeMenu.testColorTheme.connect(self.applyAllStyles)

        # signal to show personal games list window
        self.tableWidget.personalGamesButtonSignal.connect(self.showEditPersonalGamesWindow)

        # show custom points value window signal
        self.pointInfoWidget.pointsAdjustmentSignal.connect(self.showCustomPointsWindow)

        # Connect the custom points value widget's pointsChangedSignal to point info widget's update points function
        self.customPointsValueWidget.pointsChangedSignal.connect(self.pointInfoWidget.updatePoints)

        # Connect signal that updates the personal game list after a game has been switched out
        self.editPersonalGamesListInfo.pListChangeSignal.connect(self.refreshPersonalListTable)

        # Connect options menu button to show the options menu
        self.optionsButton.clicked.connect(self.showOptionsWindow)

        # Connect signal that closes the options menu
        self.optionsMenu.mainMenu.closeMenuSignal.connect(self.hideOptionsWindow)

        # because I wanted to have both the points widget and weekly information widget below the tables
        # I combined these two widgets into the same layout
        self.informationButtonLayout.addWidget(self.pointInfoWidget)
        self.informationButtonLayout.addWidget(self.timeSensitiveInfoWidget)

        # set the widgets into the main layout
        self.mainLayout.addWidget(self.tableWidget, 0, 0)
        self.mainLayout.addLayout(self.informationButtonLayout, 1, 0)
        self.mainLayout.addLayout(self.extraSettingsBar, 2, 0)

        # set main layout
        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)


    def showGameListWindow(self):
        self.editGameListWindow.setWindowTitle("View/Edit/Add Games")
        self.editGameListWindow.setGeometry(200, 200, 550, 550)
        self.editGameListWindow.show()
        logProcess("Opened games list window")

    def loadPreferredColorPalette(self):
        data = loadJSONData()
        self.updateColorPalette(data['savedColorPalette'])
        common.currentlyAppliedColorScheme = data['savedColorPalette']
        logProcess("Loaded saved color scheme")

    def updateColorPalette(self, colorPalette):
        with open(f'Color Palettes/{colorPalette}.css') as stylesheet:
            style = stylesheet.read()
            self.setStyleSheet(style)

    def applyAllStyles(self, palette):
        massApplyStyles(self.widgetList, palette)
        self.updateColorPalette(palette)
        self.tableWidget.applyIndividualStyling(palette.lower())
        self.editGameListWindow.applyIndividualStyling(palette.lower())
        self.customPointsValueWidget.applyIndividualStyling(palette.lower())
        logProcess(f"Applied ({palette}) to program")

    def showEditPersonalGamesWindow(self):
        self.editPersonalGamesListInfo.setWindowTitle("Edit Personal Games List")
        self.editPersonalGamesListInfo.setGeometry(200, 200, 350, 290)
        self.editPersonalGamesListInfo.show()

    def showCustomPointsWindow(self):
        # create and show the window itself
        self.customPointsValueWidget.setWindowTitle("Add Custom Points Value")
        self.customPointsValueWidget.setGeometry(200, 200, 200, 150)
        self.customPointsValueWidget.show()

    def refreshPersonalListTable(self):
        self.tableWidget.loadPersonalList()
        logProcess("Refreshed personal games list")

    def showCustomStylingNameWindow(self):
        self.customStyleSheetNamingWindow.show()

    def showOptionsWindow(self):
        self.optionsMenu.setWindowTitle("Options")
        self.optionsMenu.setGeometry(200, 200, 550, 550)
        self.optionsMenu.show()

    def hideOptionsWindow(self):
        self.optionsMenu.hide()

    def quitApplication(self):
        logProcess("Closing application")
        QApplication.quit()



def main():
    app = QApplication(sys.argv)
    mainApplication = MainApplication()
    mainApplication.loadPreferredColorPalette()
    massApplyStyles(mainApplication.getWidgetList(), loadColorPallet())
    mainApplication.show()
    sys.exit((app.exec_()))

if __name__ == "__main__":
    main()

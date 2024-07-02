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
    # signal for styling application
    applyStylingSignal = pyqtSignal()

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
            self.optionsMenu,
        ]

        self.signalConnections = [
            (self.optionsMenu.colorThemeMenu.testColorTheme, self.applyAllStyles),
            (self.tableWidget.personalGamesButtonSignal, self.showEditPersonalGamesWindow),
            (self.pointInfoWidget.pointsAdjustmentSignal, self.showCustomPointsWindow),
            (self.customPointsValueWidget.pointsChangedSignal, self.pointInfoWidget.updatePoints),
            (self.editPersonalGamesListInfo.pListChangeSignal, self.refreshPersonalListTable),
            (self.optionsButton.clicked, self.showOptionsWindow),
            (self.optionsMenu.mainMenu.closeMenuSignal, self.hideOptionsWindow),
            (self.optionsMenu.mainMenu.closeApplicationSignal, self.showApplicationResetWindow),
            (self.applyStylingSignal, self.loadAllStyling),
            (self.editGameListWindow.updateTableSignal, self.tableWidget.loadStoredTablesSignalMethod),
            (self.optionsMenu.toggleWidgetsMenu.pointsUISignal, self.adjustPointsUI),
            (self.optionsMenu.toggleWidgetsMenu.dailyWeeklySignal, self.adjustDailyWeeklyUI)
        ]

        for signal, slot in self.signalConnections:
            signal.connect(slot)



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

    def loadAllStyling(self):
        data = loadJSONData()
        savedPalette = data['savedColorPalette']
        self.applyAllStyles(savedPalette)

    def applyAllStyles(self, palette):
        massApplyStyles(self.widgetList, palette)
        self.updateColorPalette(palette)
        self.tableWidget.applyIndividualStyling(palette.lower())
        self.editGameListWindow.applyIndividualStyling(palette.lower())
        self.customPointsValueWidget.applyIndividualStyling(palette.lower())
        self.editPersonalGamesListInfo.swapInMenu.styleInputField(palette.lower())
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

    def showApplicationResetWindow(self):
        resetWindowConfirmation = QMessageBox()
        resetWindowConfirmation.setText("Saved data has been fully reset, this application will close now.")
        resetWindowConfirmation.setWindowTitle("Restart Notice")
        resetWindowConfirmation.setStandardButtons(QMessageBox.Ok)

        returnValue = resetWindowConfirmation.exec_()

        if returnValue == QMessageBox.Ok:
            self.quitApplication()

    def adjustPointsUI(self, signalPing):
        if not signalPing:
            self.pointInfoWidget.hide()
        else:
            self.pointInfoWidget.show()

    def adjustDailyWeeklyUI(self, signalPing):
        if not signalPing:
            self.timeSensitiveInfoWidget.hide()



def main():
    app = QApplication(sys.argv)
    mainApplication = MainApplication()
    mainApplication.loadPreferredColorPalette()
    mainApplication.applyStylingSignal.emit()
    massApplyStyles(mainApplication.getWidgetList(), loadColorPallet())
    mainApplication.show()
    sys.exit((app.exec_()))


if __name__ == "__main__":
    main()

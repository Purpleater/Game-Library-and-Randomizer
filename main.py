import os

from PyQt5.QtCore import QCoreApplication

from common import *

# import Widgets
from Widgets.TablesWidget import TablesWidget
from Widgets.PointsAdjustmentWidget import PointsAdjustmentWidget
from Widgets.TimeSensitiveInfoWidget import TimeSensitiveInfoWidget
from Widgets.EditGamesWindow import EditGameWindow
from Widgets.ColorModeSelectionWindow import ColorSelectionWindow


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Main Application")
        self.setGeometry(100, 100, 800, 855)

        # create layout
        self.mainLayout = QGridLayout()
        self.informationButtonLayout = QHBoxLayout()
        self.extraSettingsBar = QHBoxLayout()

        # create buttons for extras and settings

        self.editGameListInformationButton = QPushButton("Edit/Add To Game List")
        self.paletteSettingsButton = QPushButton("Change UI Color Palette")
        self.exitButton = QPushButton("Exit Program")

        # connect buttons to methods
        self.editGameListInformationButton.clicked.connect(self.showGameListWindow)
        self.exitButton.clicked.connect(self.quitApplication)
        self.paletteSettingsButton.clicked.connect(self.showColorChangeWindow)


        # add extra settings buttons to layout

        self.extraSettingsBar.addWidget(self.editGameListInformationButton)
        self.extraSettingsBar.addWidget(self.paletteSettingsButton)
        self.extraSettingsBar.addWidget(self.exitButton)

        # initialize the windows within the scope of the main application
        self.tableWidget = TablesWidget()
        self.tableWidget.setObjectName("tableWidget")

        self.pointInfoWidget = PointsAdjustmentWidget()
        self.pointInfoWidget.setObjectName("pointInfoWidget")

        self.timeSensitiveInfoWidget = TimeSensitiveInfoWidget()
        self.timeSensitiveInfoWidget.setObjectName("timeSensitiveInfoWidget")

        self.editGameListWindow = EditGameWindow()
        self.editGameListWindow.setObjectName("editGameListWindow")

        self.colorSelectionWindow = ColorSelectionWindow()
        self.colorSelectionWindow.setObjectName("colorSelectionWindow")

        # color selected signal
        self.colorSelectionWindow.colorSelection.connect(self.updateColorPalette)


        # because I wanted to have both the points widget and weekly information widget below the tables
        # I combined these two widgets into the same layout
        self.informationButtonLayout.addWidget(self.pointInfoWidget)
        self.informationButtonLayout.addWidget(self.timeSensitiveInfoWidget)

        # set the widgets into the main layout
        self.mainLayout.addWidget(self.tableWidget, 0, 0)
        self.mainLayout.addLayout(self.informationButtonLayout, 1, 0)
        self.mainLayout.addLayout(self.extraSettingsBar, 2, 0)

        # set preferred color palette on load
        self.loadPreferredColorPalette()
        ''''''
        # set main layout
        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

    def showGameListWindow(self):
        self.editGameListWindow.setWindowTitle("View/Edit/Add Games")
        self.editGameListWindow.setGeometry(200, 200, 550, 550)
        self.editGameListWindow.show()

    def showColorChangeWindow(self):
        self.colorSelectionWindow.setWindowTitle("Select UI Color Palette")
        self.colorSelectionWindow.setGeometry(200, 200, 550, 550)
        self.colorSelectionWindow.show()

    def loadPreferredColorPalette(self):
        data = loadJSONData()
        self.updateColorPalette(data['savedColorPalette'])

    def updateColorPalette(self, colorPalette):
        with open(f'Color Palettes/{colorPalette}.css') as stylesheet:
            style = stylesheet.read()
            self.setStyleSheet(style)
            self.editGameListWindow.setStyleSheet(style)
            self.timeSensitiveInfoWidget.setStyleSheet(style)


    def quitApplication(self):
        QApplication.quit()




def main():
    app = QApplication(sys.argv)
    mainApplication = MainApplication()
    mainApplication.show()
    sys.exit((app.exec_()))


if __name__ == "__main__":
    main()

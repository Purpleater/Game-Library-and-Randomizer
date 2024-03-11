from common import *
from Widgets.CustomPointsValueWindow import CustomPointsValueWidget


class PointsAdjustmentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.mainLayout = QVBoxLayout()

        # create widgets
        self.pointsLabel = QLabel(f"# of Points:\n\n"
                                  f"__{getNumberOfPointsFromFile()}__")
        self.pointsLabel.setAlignment(Qt.AlignCenter)

        self.addOnePointButton = QPushButton("Add 1 Point")
        self.addOnePointButton.clicked.connect(self.addOnePoint)

        self.addTwoPointsButton = QPushButton("Add 2 Points")
        self.addTwoPointsButton.clicked.connect(self.addTwoPoints)

        self.addCustomValue = QPushButton("Custom Value")
        self.addCustomValue.clicked.connect(self.showCustomPointsValueWindow)

        # add widgets to layout

        self.mainLayout.addWidget(self.pointsLabel)
        self.mainLayout.addWidget(self.addOnePointButton)
        self.mainLayout.addWidget(self.addTwoPointsButton)
        self.mainLayout.addWidget(self.addCustomValue)

        # create class instance of the custom points value window for signal connection

        self.customPointsValueWindow = CustomPointsValueWidget()

        # set the signal slot
        self.customPointsValueWindow.pointsChanged.connect(self.updatePoints)

        # set main layout
        self.setLayout(self.mainLayout)

        # set stylesheet
        setStyle(self, loadColorPallet())

    def addOnePoint(self):
        with open('ApplicationInformation.json', 'r') as file:
            data = json.load(file)
            data['numberOfPoints'] += 1

        updateJSONData(data)
        self.pointsLabel.setText((f"# of Points: \n\n"
                                  f"__{getNumberOfPointsFromFile()}__"))

    def addTwoPoints(self):
        with open('ApplicationInformation.json', 'r') as file:
            data = json.load(file)
            data['numberOfPoints'] += 2

        updateJSONData(data)

        self.pointsLabel.setText((f"# of Points: \n\n"
                                  f"__{getNumberOfPointsFromFile()}__"))

    def showCustomPointsValueWindow(self):
        # generate the object
        self.customPointsValueWindow = CustomPointsValueWidget()
        self.customPointsValueWindow.setObjectName("customPointValueWindow")

        # create and show the window itself
        self.customPointsValueWindow.setWindowTitle("Add Custom Points Value")
        self.customPointsValueWindow.setGeometry(200, 200, 200, 150)
        self.customPointsValueWindow.show()

    def updatePoints(self, pointsSignal):
        self.pointsLabel.setText(f"# of Points:\n\n"
                                 f"__{pointsSignal}__")

from common import *
from Widgets.CustomPointsValueWindow import CustomPointsValueWidget


class PointsAdjustmentWidget(QWidget):
    pointsAdjustmentSignal = pyqtSignal()
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

        # set main layout
        self.setLayout(self.mainLayout)


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
        self.pointsAdjustmentSignal.emit()

    def updatePoints(self, string):
        print(string)

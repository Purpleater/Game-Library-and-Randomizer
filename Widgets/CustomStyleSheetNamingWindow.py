from common import *

class CustomStyleSheetNamingWindow(QWidget):
    addStyleSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.mainLayout = QVBoxLayout()
        self.inputForm = QHBoxLayout()

        self.nameInput = QLineEdit()

        self.promptLabel = QLabel("Please provide a name for your style sheet: ")
        self.submitButton = QPushButton("Submit")

        # connect button to function
        self.submitButton.clicked.connect(self.submitInformation)

        # connect input field
        self.nameInput.textChanged.connect(self.checkIfInputFieldHasCharacters)

        # set button as initially disabled until stuff is typed in the field
        self.submitButton.setEnabled(False)

        self.inputForm.addWidget(self.promptLabel)
        self.inputForm.addWidget(self.nameInput)

        self.mainLayout.addLayout(self.inputForm)
        self.mainLayout.addWidget(self.submitButton)

        self.setLayout(self.mainLayout)

    def checkIfInputFieldHasCharacters(self):
        nameInput = self.nameInput.text()
        if len(nameInput) <= 0:
            self.submitButton.setEnabled(False)
        else:
            self.submitButton.setEnabled(True)

    def submitInformation(self):
        data = loadJSONData()
        nameInput = self.nameInput.text()

        for item in data["colorPaletteList"]:
            if nameInput.lower() == item.lower():
                alertMessage = QMessageBox()
                alertMessage.setText("The name that you have provided already exists within the given directory")
                alertMessage.exec_()
                self.nameInput.clear()
                break
        splitString = nameInput.split(" ")
        finalString = ''
        for item in splitString:
            if item != splitString[-1]:
                finalString += item
                finalString += "-"
            else:
                finalString += item
        data["colorPaletteList"].append(finalString)
        updateJSONData(data)
        self.addStyleSignal.emit()










from common import *

class CustomStyleSheetNamingWindow(QWidget):
    addStyleSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        self.mainLayout = QStackedLayout()

        # __1st layout (naming the stylesheet itself)__
        self.menu1Widget = QWidget()
        self.menu1MainLayout = QVBoxLayout()
        self.menu1FormLayout = QHBoxLayout()
        self.styleSheetNameInput = QLineEdit()

        self.sheetNamePromptLabel = QLabel("Please provide a name for your style sheet: ")
        self.sheetNameSubmitButton = QPushButton("Submit")

        # fix this later
        self.sheetNameSubmitButton.setEnabled(False)

        self.styleSheetNameInput.textChanged.connect(self.checkIfInputFieldHasCharacters)
        self.sheetNameSubmitButton.clicked.connect(self.showLineEditInformationWindow)

        self.menu1FormLayout.addWidget(self.sheetNamePromptLabel)
        self.menu1FormLayout.addWidget(self.styleSheetNameInput)
        self.menu1MainLayout.addLayout(self.menu1FormLayout)
        self.menu1MainLayout.addWidget(self.sheetNameSubmitButton)
        self.menu1Widget.setLayout(self.menu1MainLayout)

        # __2nd Layout (Input field styling)__
        self.menu2Widget = QWidget()
        self.menu2MainLayout = QVBoxLayout()

        self.lineEditTextColorRow = QHBoxLayout()
        self.lineEditTextColorInput = QLineEdit()
        self.lineEditTextColorRow.addWidget(QLabel("Text Color Hex: #"))
        self.lineEditTextColorRow.addWidget(self.lineEditTextColorInput)

        self.lineEditBorderColorRow = QHBoxLayout()
        self.lineEditBorderColorInput = QLineEdit()
        self.lineEditBorderColorRow.addWidget(QLabel("Border Color Hex: #"))
        self.lineEditBorderColorRow.addWidget(self.lineEditBorderColorInput)

        self.lineEditButtonRow = QHBoxLayout()
        self.lineEditBackButton = QPushButton("Back")
        self.lineEditSubmissionButton = QPushButton("Submit")

        self.lineEditSubmissionButton.clicked.connect(self.showTableCornerInformationWindow)
        self.lineEditBackButton.clicked.connect(self.showStylesheetNamingMenu)

        self.lineEditButtonRow.addWidget(self.lineEditBackButton)
        self.lineEditButtonRow.addWidget(self.lineEditSubmissionButton)

        self.menu2MainLayout.addLayout(self.lineEditTextColorRow)
        self.menu2MainLayout.addLayout(self.lineEditBorderColorRow)
        self.menu2MainLayout.addLayout(self.lineEditButtonRow)
        self.menu2Widget.setLayout(self.menu2MainLayout)

        # __3rd Layout (Table corner styling)__

        self.menu3Widget = QWidget()
        self.menu3MainLayout = QVBoxLayout()

        self.tableCornerFormRow = QHBoxLayout()
        self.tableCornerColorInput = QLineEdit()
        self.tableCornerFormRow.addWidget(QLabel("Table Corner Hex: #"))
        self.tableCornerFormRow.addWidget(self.tableCornerColorInput)

        self.tableCornerColorInput.textChanged.connect(self.checkIfInputFieldHasCharacters)

        self.tableCornerButtonRow = QHBoxLayout()
        self.tableCornerBackButton = QPushButton("Back")
        self.tableCornerSubmitButton = QPushButton("Submit")


        self.tableCornerBackButton.clicked.connect(self.showLineEditInformationWindow)

        self.menu3MainLayout.addLayout(self.tableCornerFormRow)
        self.menu3MainLayout.addLayout(self.tableCornerButtonRow)
        self.menu3Widget.setLayout(self.menu3MainLayout)

        # __4th Layout (Combo Box Styling)__
        self.menu4Widget = QWidget()
        self.menu4MainLayout = QVBoxLayout()

        self.comboBoxBorderColorRow= QHBoxLayout()
        self.comboBoxBorderColorInput = QLineEdit()
        self.comboBoxBorderColorRow.addWidget(QLabel("Border Color Hex: #"))
        self.comboBoxBorderColorRow.addWidget(self.comboBoxBorderColorInput)

        self.comboBoxTextColorRow= QHBoxLayout()
        self.comboBoxTextColorInput = QLineEdit()
        self.comboBoxTextColorRow.addWidget(QLabel("Text Color Hex: #"))
        self.comboBoxTextColorRow.addWidget(self.comboBoxTextColorInput)

        self.comboBoxTextColorRow= QHBoxLayout()
        self.comboBoxFontWeightList = QComboBox()
        self.comboBoxTextColorRow.addWidget(QLabel("Text Color Hex: #"))
        self.comboBoxTextColorRow.addWidget(self.comboBoxTextColorInput)


        # add menu widgets
        self.mainLayout.addWidget(self.menu1Widget)
        self.mainLayout.addWidget(self.menu2Widget)
        self.mainLayout.addWidget(self.menu3Widget)

        self.setLayout(self.mainLayout)


    def checkIfInputFieldHasCharacters(self, widget):
        nameInput = self.styleSheetNameInput.text()
        if len(nameInput) <= 0:
            self.sheetNameSubmitButton.setEnabled(False)
        else:
            self.sheetNameSubmitButton.setEnabled(True)

    def submitSheetNameInformation(self):
        self.showLineEditInformationWindow()
        '''
                data = loadJSONData()
        nameInput = self.styleSheetNameInput.text()

        for item in data["colorPaletteList"]:
            if nameInput.lower() == item.lower():
                alertMessage = QMessageBox()
                alertMessage.setText("The name that you have provided already exists within the given directory")
                alertMessage.exec_()
                self.styleSheetNameInput.clear()
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
        # updateJSONData(data)
        self.addStyleSignal.emit()
        '''
    def showStylesheetNamingMenu(self):
        self.mainLayout.setCurrentIndex(0)

    def showLineEditInformationWindow(self):
        self.mainLayout.setCurrentIndex(1)

    def showTableCornerInformationWindow(self):
        self.mainLayout.setCurrentIndex(2)











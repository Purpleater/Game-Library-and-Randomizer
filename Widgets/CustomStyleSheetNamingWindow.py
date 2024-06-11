from common import *

comboBoxFontWeightRef = {
    0: "N/A",
    1: "",
    2: "font-weight: bold;"
}

class Stylesheet:
    def __init__(self, name, file, inputLineStylingList, tableCornerColor, comboBoxStylingList):
        self.name = name
        self.file = file
        self.inputStyling = inputLineStylingList
        self.tableCornerColor = tableCornerColor
        self.comboBoxStyling = comboBoxStylingList

    def toJSON(self):
        return {
            "name": self.name,
            "file": self.file,
            "inputLineStyling": self.inputStyling,
            "tableCornerColor": self.tableCornerColor,
            "comboBoxStyling": self.comboBoxStyling
        }

class CustomStyleSheetNamingWindow(QWidget):
    addStyleSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.widgetUI()

        self.styleSheetName = ''
        self.styleSheetFileName = ''
        self.inputLineStylingList = []
        self.tableCornerColor = ''
        self.comboBoxStylingList = []
        self.styleSheetFilePath = ''

    def widgetUI(self):
        self.mainLayout = QStackedLayout()

        # __1st layout (naming the stylesheet itself)__
        self.menu1Widget = QWidget()
        self.menu1MainLayout = QVBoxLayout()
        self.menu1FormLayout = QHBoxLayout()
        self.styleSheetNameInput = QLineEdit()

        self.sheetNamePromptLabel = QLabel("Please provide a name for your style sheet: ")
        self.sheetNameSubmitButton = QPushButton("Submit")

        self.sheetNameSubmitButton.setEnabled(False)

        self.styleSheetNameInput.textChanged.connect(self.checkIfFileNameInputHasCharacters)
        self.sheetNameSubmitButton.clicked.connect(self.submitFileNameInformation)

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
        self.lineEditTextColorInput.setMaxLength(6)
        self.lineEditTextColorRow.addWidget(QLabel("Text Color Hex: #"))
        self.lineEditTextColorRow.addWidget(self.lineEditTextColorInput)
        self.lineEditTextColorInput.textChanged.connect(self.checkIfInputFieldStyleFieldsHaveCharacters)

        self.lineEditBorderColorRow = QHBoxLayout()
        self.lineEditBorderColorInput = QLineEdit()
        self.lineEditBorderColorInput.setMaxLength(6)
        self.lineEditBorderColorRow.addWidget(QLabel("Border Color Hex: #"))
        self.lineEditBorderColorRow.addWidget(self.lineEditBorderColorInput)
        self.lineEditBorderColorInput.textChanged.connect(self.checkIfInputFieldStyleFieldsHaveCharacters)

        self.lineEditButtonRow = QHBoxLayout()
        self.lineEditBackButton = QPushButton("Back")
        self.lineEditSubmissionButton = QPushButton("Submit")
        self.lineEditSubmissionButton.setEnabled(False)

        self.lineEditSubmissionButton.clicked.connect(self.submitInputFieldStylingInformation)
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
        self.tableCornerColorInput.setMaxLength(6)
        self.tableCornerFormRow.addWidget(QLabel("Table Corner Hex: #"))
        self.tableCornerFormRow.addWidget(self.tableCornerColorInput)

        self.tableCornerColorInput.textChanged.connect(self.checkIfTableCornerFieldHasCharacters)

        self.tableCornerButtonRow = QHBoxLayout()
        self.tableCornerBackButton = QPushButton("Back")
        self.tableCornerSubmitButton = QPushButton("Submit")
        self.tableCornerButtonRow.addWidget(self.tableCornerBackButton)
        self.tableCornerButtonRow.addWidget(self.tableCornerSubmitButton)
        self.tableCornerSubmitButton.setEnabled(False)

        self.tableCornerBackButton.clicked.connect(self.showLineEditInformationWindow)
        self.tableCornerSubmitButton.clicked.connect(self.submitTableCornerInformation)

        self.menu3MainLayout.addLayout(self.tableCornerFormRow)
        self.menu3MainLayout.addLayout(self.tableCornerButtonRow)
        self.menu3Widget.setLayout(self.menu3MainLayout)

        # __4th Layout (Combo Box Styling)__
        self.menu4Widget = QWidget()
        self.menu4MainLayout = QVBoxLayout()

        self.comboBoxBorderColorRow= QHBoxLayout()
        self.comboBoxBorderColorInput = QLineEdit()
        self.comboBoxBorderColorInput.setMaxLength(6)
        self.comboBoxBorderColorRow.addWidget(QLabel("Border Color Hex: #"))
        self.comboBoxBorderColorRow.addWidget(self.comboBoxBorderColorInput)
        self.comboBoxBorderColorInput.textChanged.connect(self.checkIfAllComboBoxInformationIsComplete)

        self.comboBoxTextColorRow= QHBoxLayout()
        self.comboBoxTextColorInput = QLineEdit()
        self.comboBoxTextColorInput.setMaxLength(6)
        self.comboBoxTextColorRow.addWidget(QLabel("Text Color Hex: #"))
        self.comboBoxTextColorRow.addWidget(self.comboBoxTextColorInput)
        self.comboBoxBorderColorInput.textChanged.connect(self.checkIfAllComboBoxInformationIsComplete)

        self.comboBoxFontWeightRow= QHBoxLayout()
        self.comboBoxFontWeightList = QComboBox()
        self.comboBoxFontWeightRow.addWidget(QLabel("Font Weight: "))
        self.comboBoxFontWeightRow.addWidget(self.comboBoxFontWeightList)
        self.comboBoxFontWeightList.addItems(["Select Option", "None", "Bold"])
        self.comboBoxFontWeightList.currentIndexChanged.connect(self.checkIfAllComboBoxInformationIsComplete)

        self.menu4MainLayout.addLayout(self.comboBoxBorderColorRow)
        self.menu4MainLayout.addLayout(self.comboBoxTextColorRow)
        self.menu4MainLayout.addLayout(self.comboBoxFontWeightRow)

        self.comboBoxButtonRow = QHBoxLayout()
        self.comboBoxBackButton = QPushButton("Back")
        self.comboBoxSubmitButton = QPushButton("Submit")
        self.comboBoxButtonRow.addWidget(self.comboBoxBackButton)
        self.comboBoxButtonRow.addWidget(self.comboBoxSubmitButton)
        self.comboBoxSubmitButton.setEnabled(False)

        self.comboBoxBackButton.clicked.connect(self.showTableCornerInformationWindow)
        self.comboBoxSubmitButton.clicked.connect(self.submitComboBoxInformation)

        self.menu4MainLayout.addLayout(self.comboBoxBorderColorRow)
        self.menu4MainLayout.addLayout(self.comboBoxTextColorRow)
        self.menu4MainLayout.addLayout(self.comboBoxFontWeightRow)
        self.menu4MainLayout.addLayout(self.comboBoxButtonRow)

        self.menu4Widget.setLayout(self.menu4MainLayout)

        # add menu widgets
        self.mainLayout.addWidget(self.menu1Widget)
        self.mainLayout.addWidget(self.menu2Widget)
        self.mainLayout.addWidget(self.menu3Widget)
        self.mainLayout.addWidget(self.menu4Widget)

        self.setLayout(self.mainLayout)


    def checkIfFileNameInputHasCharacters(self):
        nameInput = self.styleSheetNameInput.text()
        if len(nameInput) <= 0:
            self.sheetNameSubmitButton.setEnabled(False)
        else:
            self.sheetNameSubmitButton.setEnabled(True)

    def submitFileNameInformation(self):
        validation = True
        self.styleSheetName = self.styleSheetNameInput.text()
        for item in loadJSONData()["colorPaletteList"]:
            if self.styleSheetName.lower() == item["name"].lower():
                alertMessage = QMessageBox()
                alertMessage.setText("The name that you have provided already exists within the given directory")
                alertMessage.exec_()
                self.styleSheetNameInput.clear()
                validation = False
        if validation:
            self.showLineEditInformationWindow()

    def checkIfInputFieldStyleFieldsHaveCharacters(self):
        textColorInput = self.lineEditTextColorInput.text()
        borderColorInput = self.lineEditBorderColorInput.text()

        if len(textColorInput) == 0 or len(borderColorInput) == 0:
            self.lineEditSubmissionButton.setEnabled(False)
        else:
            self.lineEditSubmissionButton.setEnabled(True)

    def submitInputFieldStylingInformation(self):
        inputFieldTextColor = self.lineEditTextColorInput.text()
        inputFieldBorderColor = self.lineEditBorderColorInput.text()
        self.inputLineStylingList = [f'#{inputFieldTextColor}', f'#{inputFieldBorderColor}']
        self.showTableCornerInformationWindow()

    def checkIfTableCornerFieldHasCharacters(self):
        tableCornerInput = self.tableCornerColorInput.text()

        if len(tableCornerInput) == 0:
            self.tableCornerSubmitButton.setEnabled(False)
        else:
            self.tableCornerSubmitButton.setEnabled(True)

    def submitTableCornerInformation(self):
        tableCornerColor = self.tableCornerColorInput.text()
        self.tableCornerColor = f'#{tableCornerColor}'
        self.showComboBoxInformationWindow()

    def checkIfAllComboBoxInformationIsComplete(self):
        comboBoxBorderInput = self.comboBoxBorderColorInput.text()
        comboBoxTextColorInput = self.comboBoxTextColorInput.text()
        comboBoxFontWeightSelection = self.comboBoxFontWeightList.currentIndex()

        comboBoxFontWeightSelection = comboBoxFontWeightRef[comboBoxFontWeightSelection]
        if len(comboBoxBorderInput) == 0 or len(comboBoxTextColorInput) == 0 or comboBoxFontWeightSelection == 'N/A':
            self.comboBoxSubmitButton.setEnabled(False)
        else:
            self.comboBoxSubmitButton.setEnabled(True)

    def submitComboBoxInformation(self):
        comboBoxBorderColor = self.comboBoxBorderColorInput.text()
        comboBoxTextColor = self.comboBoxTextColorInput.text()
        comboBoxFontWeight = self.comboBoxFontWeightList.currentIndex()

        self.comboBoxStylingList = [f'#{comboBoxBorderColor}', f'#{comboBoxTextColor}', comboBoxFontWeightRef[comboBoxFontWeight]]
        self.submitFullSheetInformation()

    def submitFullSheetInformation(self):

        newStyleSheet = Stylesheet(
            self.styleSheetName,
            self.styleSheetFileName,
            self.inputLineStylingList,
            self.tableCornerColor,
            self.comboBoxStylingList
        )

        if self.showStylingConfirmationWindow():
            showProcessConfirmationWindow(f"Addition of the ({self.styleSheetName}) file successful")
            data = loadJSONData()
            data["colorPaletteList"].append(newStyleSheet.toJSON())
            updateJSONData(data)
            shutil.copy(self.styleSheetFilePath, 'Color Palettes')





        '''
                data = loadJSONData()
        nameInput = self.styleSheetNameInput.text()

        
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

    def showComboBoxInformationWindow(self):
        self.mainLayout.setCurrentIndex(3)

    def showStylingConfirmationWindow(self):
        textString = f"Does the following information look correct?\n\n" \
                     f"Stylesheet Name: ({self.styleSheetName})\nStylesheet Filepath: ({self.styleSheetFilePath})\n\n" \
                     f"Input field text color: ({self.inputLineStylingList[0]})\n Input field border color: ({self.inputLineStylingList[1]})\n\n" \
                     f"Table Corner Color: ({self.tableCornerColor})\n\n" \
                     f"Combo Box Border Color: ({self.comboBoxStylingList[0]})\nCombo Box Text Color: ({self.comboBoxStylingList[1]})\n Combo Box Font Weight: ({self.comboBoxStylingList[2]})"
        windowTitle = "Stylesheet Info Confirmation"
        trueProcessArray = []
        falseProcessArray = []
        return createStandardConfirmationWindow(textString, windowTitle, trueProcessArray, falseProcessArray)











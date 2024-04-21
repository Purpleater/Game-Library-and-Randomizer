from common import *

class CustomStyleSheetNamingWindow(QWidget):

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

        self.inputForm.addWidget(self.promptLabel)
        self.inputForm.addWidget(self.nameInput)


        self.mainLayout.addLayout(self.inputForm)
        self.mainLayout.addWidget(self.submitButton)

        self.setLayout(self.mainLayout)


    def submitInformation(self):
        printMeese()



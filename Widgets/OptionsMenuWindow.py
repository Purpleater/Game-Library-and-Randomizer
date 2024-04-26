from common import *

class OptionsMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.widgetUI()

    def widgetUI(self):
        # initialize main layout
        self.mainLayout = QVBoxLayout()

        # initialize buttons
        self.colorPaletteButton = QPushButton("Change UI Color Theme")

        # TODO: Add "Change UI Theme", "Toggle (x) Widget(s)"
        self.mainLayout.addWidget(self.colorPaletteButton)

        #set main layout
        self.setLayout(self.mainLayout)
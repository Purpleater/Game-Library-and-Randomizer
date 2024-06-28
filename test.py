from common import *

'''

import re


def is_valid_hexa_code(string):
    hexa_code = re.compile(r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$')
    return bool(re.match(hexa_code, string))

string = "#100"
print(is_valid_hexa_code(string))
'''

class TestClass(QObject):  # Inherit from QObject to use signals

    testSignal = pyqtSignal()  # Define the signal as a class attribute

    def __init__(self):
        super().__init__()  # Call the superclass's constructor

    def emitSignal(self):
        self.testSignal.emit()


class OtherTestClass:

    def __init__(self):
        self.firstTestClass = TestClass()  # Store the instance in an attribute
        self.firstTestClass.testSignal.connect(self.printMeese)

    def printMeese(self):
        print("Signal received!")


# Create an instance of OtherTestClass, which sets up the signal connection
other_test_instance = OtherTestClass()

# Emit the signal using the instance of TestClass stored in OtherTestClass
other_test_instance.firstTestClass.emitSignal()



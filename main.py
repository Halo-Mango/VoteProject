"""
This file starts the Application
It sets it up shows the main window, and runs the app
The logic import imports the logic file that helps the app run
"""
from logic import *
def main():
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()

if __name__ == '__main__':
    main()
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QMessageBox
from gui import *
import csv


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        This starts the application, sets up the window,
        clears the voter_info.csv data, and then connects
        all the buttons to their actions
        """
        super().__init__()

        open("voter_info.csv", 'w').close()
        self.setupUi(self)

        self.pushButton_vote.clicked.connect(self.voting_page)
        self.pushButton_exit.clicked.connect(self.results_page)
        self.pushButton_submit.clicked.connect(self.submit_vote)

    def voting_page(self) -> None:
        """
        This displays the page where the user can
        pick to vote or exit the application.
        """
        self.stackedWidget.setCurrentIndex(1)

    def results_page(self) -> None:
        """
        Show the page where the user can see all who voted
        """
        self.stackedWidget.setCurrentIndex(2)
        self.load_results()


    def submit_vote(self) -> None:
        """
        This handles the votes submitted it checks to make sure
        what is typed in Voter ID is in a valid format,
        Ensures the voter has not already put a vote in,
        and Makes sure once an ID has been entered a candidate
        is also picked, writes the vote to the CSV file voter_info.csv
        it also gives user errors in the form of a message box.
        """
        voter_id = self.id_input.text().strip()
        if not voter_id.isdigit():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Voter ID must contain only numbers.")
            msg.setWindowTitle("Invalid Input")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        if not voter_id:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Voter ID is required.")
            msg.setWindowTitle("Invalid Input")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return
        try:
            with open("voter_info.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == voter_id:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Icon.Warning)
                        msg.setText("This Voter ID has already voted.")
                        msg.setWindowTitle("Duplicate Vote")
                        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                        msg.exec()
                        return
        except FileNotFoundError:
            pass

        if self.jane_button.isChecked():
            vote = "JANE"
        elif self.john_button.isChecked():
            vote = "JOHN"
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Please select a candidate.")
            msg.setWindowTitle("Input Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        try:
            with open("voter_info.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([voter_id, vote])

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Your vote has been recorded.")
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

            self.stackedWidget.setCurrentIndex(0)
            self.reset_page_input()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Failed to record vote.")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()




    def reset_page_input(self):
        self.user_id.clear()  # clear after submission
        self.jane_button.setChecked(False)
        self.john_button.setChecked(False)

    def load_results(self) -> None:
        """
        This loads the results from the voter_info.csv file and
        shows them in the QListView widget which displays the data.
        """
        try:
            with open("voter_info.csv", mode="r") as file:
                reader = csv.reader(file)
                lines = [f"Voter ID: {row[0]:<55} | Vote: {row[1]}" for row in reader]
            model = QStringListModel()
            model.setStringList(lines)
            self.votes_view.setModel(model)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Could not load vote results.")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton)
            msg.exec()
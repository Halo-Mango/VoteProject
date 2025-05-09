from PyQt6.QtWidgets import *
from gui import *
import csv

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        open("voter_info.csv", 'w').close()

        self.setupUi(self)

        self.pushButton_vote.clicked.connect(self.voting_page)
        self.pushButton_exit.clicked.connect(self.results_page)
        self.pushButton_submit.clicked.connect(self.submit_vote)

    def voting_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def results_page(self):
        self.stackedWidget.setCurrentIndex(2)
        self.load_results()


    def submit_vote(self):
        voter_id = self.id_input.text().strip()
        if not voter_id.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Voter ID must contain only numbers.")
            return

        if not voter_id:
            QMessageBox.warning(self, 'Invalid Input', "Voter ID is required")
            # 2. Check length
        if len(voter_id) > 8:
            QMessageBox.warning(self, "Invalid Input", "Voter ID cannot be more than 8 digits.")
            return

            # 3. Check for duplicate ID
        try:
            with open("voter_info.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == voter_id:
                        QMessageBox.warning(self, "Duplicate Vote", "This Voter ID has already voted.")
                        return
        except FileNotFoundError:
            # It's okay if the file doesn't exist yet
            pass

            # 4. Check if candidate is selected
        if self.jane_button.isChecked():
            vote = "JANE"
        elif self.john_button.isChecked():
            vote = "JOHN"
        else:
            QMessageBox.warning(self, "Input Error", "Please select a candidate.")
            return


        try:
            with open("voter_info.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([voter_id, vote])
            QMessageBox.information(self, "Success", "Your vote has been recorded.")
            self.user_id.clear()  # clear after submission
            self.jane_button.setChecked(False)
            self.john_button.setChecked(False)
            self.stackedWidget.setCurrentIndex(0)  # go back to main menu
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to record vote:\n{e}")

    def load_results(self):
        try:
            with open("voter_info.csv", mode="r") as file:
                reader = csv.reader(file)
                lines = [f"Voter ID: {row[0]:<55} | Vote: {row[1]}" for row in reader]

            model = QStringListModel()
            model.setStringList(lines)
            self.votes_view.setModel(model)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load vote results:\n{e}")
# -------------------------------------------------------------------------------
# Name: Alexander Santana
# Date: 10/3/2024
# Assignment: Exam 3 - GUI for State Flag Program.
# Description: produce an application that displays state flags and description.
# -------------------------------------------------------------------------------

import sys
from PyQt6.QtWidgets import QDialog, QApplication, QComboBox, QLabel, QPushButton, QFrame
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi

# Define the main form class, extending QDialog for our window
class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        
        # Load the UI file
        self.ui = loadUi('exam3_santana.ui', self)

        # Grab the widgets from the UI by their names
        self.comboBoxState = self.ui.findChild(QComboBox, "comboBoxState")
        self.frameFlag = self.ui.findChild(QFrame, "frameFlag")
        self.labelYearAdopted = self.ui.findChild(QLabel, "labelYearAdopted")
        self.labelMajorItems = self.ui.findChild(QLabel, "labelMajorItems")
        self.exitButton = self.ui.findChild(QPushButton, "exitButton")
        
        # Create a QLabel to show the flag image inside the frame, should have watched
        # the video you made because it took me hours to learn how to make this
        self.labelImage = QLabel(self.frameFlag)
        self.labelImage.setGeometry(0, 0, self.frameFlag.width(), self.frameFlag.height())
        self.labelImage.setScaledContents(True)  # Scale image to fit

        # Allow text to wrap so it fits in the label
        self.labelMajorItems.setWordWrap(True)
        
        # Call displayFlagInfo whenever the user selects a new state
        self.comboBoxState.currentIndexChanged.connect(self.displayFlagInfo)
        
        # Close the app when the exit button is clicked
        self.exitButton.clicked.connect(self.close)
        
        # Show info for the default state (AK)
        self.displayFlagInfo()
    
    def displayFlagInfo(self):
        # Get the selected state abbreviation
        state = self.comboBoxState.currentText()

        # Info for each state, including the image file, year, and description
        state_info = {
            'AK': {
                'image': 'ak_fi.gif',
                'year': '1959',
                'description': 'The design of the official flag is eight gold stars'
                ' in a field of blue, selected for its simplicity, originality,'
                ' and symbolism. The blue represents the sky, sea, and lakes.'
            },
            'AL': {
                'image': 'al_fi.gif',
                'year': '1819',
                'description': 'The flag of Alabama features a crimson cross'
                ' of St. Andrew on a field of white. The bars form a diagonal cross.'
            },
            'AR': {
                'image': 'ar_fi.gif',
                'year': '1836',
                'description': 'The Arkansas flag has a red background with a white'
                ' diamond and a blue border with 25 stars. The word "ARKANSAS"'
                ' is displayed across the diamond.'
            },
            'NC': {
                'image': 'nc_fi.gif',
                'year': '1789',
                'description': 'North Carolina\'s flag has a blue field with a white star'
                ' and the letters "N" and "C" around it, plus red and white stripes.'
            },
            'AZ': {
                'image': 'az_fi.gif',
                'year': '1863',
                'description': 'Arizona\'s flag features a copper star in the center'
                ' with 13 red and yellow rays representing the original colonies.'
            }
        }

        # Look up the selected state's info
        info = state_info.get(state)
        if info:
            # Update the image and text labels
            pixmap = QPixmap(info['image'])
            self.labelImage.setPixmap(pixmap)
            self.labelYearAdopted.setText(info['year'])
            self.labelMajorItems.setText(info['description'])
        else:
            # Clear the image and show default text if no info
            self.labelImage.clear()
            self.labelYearAdopted.setText("N/A")
            self.labelMajorItems.setText("No info for this state.")

# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(app.exec())

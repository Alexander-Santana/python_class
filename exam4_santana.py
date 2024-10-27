# -------------------------------------------------------------------------------
# Name: Alexander Santana
# Date: 10/25/2024
# Assignment: Exam 4 Part 2 -  A Julian Date Converter Program
# Description: 
# -------------------------------------------------------------------------------

import sys  # import sys module 
from PyQt6 import QtWidgets, uic  # import QtWidgets and uic from PyQt6 to build the UI
from PyQt6.QtCore import QDate  # import QDate to work with dates

class Exam4App(QtWidgets.QDialog):  # create a class called Exam4App that inherits from QDialog
    def __init__(self):  # initialize the class
        super().__init__()  # parent class constructor
        uic.loadUi('exam4_santana.ui', self)  # load the QT designer/UI file
        
        # Connect button to methods, so they do something when clicked
        self.pushButtonConvert.clicked.connect(self.convertMethod)  # when clicked, call convertMethod
        self.pushButtonExit.clicked.connect(self.exitMethod)  # when exit clicked, call exitMethod
        
        # ***Extra credit***Show Julian date immediately when the program starts
        self.convertMethod()  # calls the convertMethod to show Julian date right away
        # and for interactivity(Kinda makes the convert method button useless but it is what it is)
        self.calendarWidget.selectionChanged.connect(self.convertMethod)  # call convertMethod when a new date is picked
        
        
        
    def convertMethod(self):  # method to convert selected date
        # Get selected date from the calendar widget
        selected_date = self.calendarWidget.selectedDate()  # get the date from the calendar
        
        # Convert to Julian date
        julian_date = selected_date.toJulianDay()  # use toJulianDay to get the Julian day number
        
        # Add commas
        formatted_julian_date = f"{julian_date:,}"  # this makes the number pretty with commas
        
        # Show the formatted Julian date in the label
        self.labelJulianDate.setText(formatted_julian_date)  # set the text of the label to the Julian date
    
    def exitMethod(self):  # method used to close application
        self.close()  # close the window when this method is called

# Run the application
if __name__ == "__main__":  
    import sys  
    app = QtWidgets.QApplication(sys.argv) 
    window = Exam4App() 
    window.show()
    sys.exit(app.exec()) 


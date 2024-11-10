# -------------------------------------------------------------------------------
# Name: Alexander Santana
# Date: November 6, 2024
# Assignment: Project 5 part 2 - GUI application to calculate distance traveled
# at speed and number of hours with a printPDF function
# Description: Calculates and displays travel distances based on speed and time,
# allows the user to save the results as a PDF.
# -------------------------------------------------------------------------------

import sys  # Importing system library for accessing command line arguments
from PyQt6.QtWidgets import QMainWindow, QApplication, QInputDialog, QListWidget, QPushButton, QDialog, QFileDialog
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog  # To print output as a pdf file
from PyQt6.QtGui import QPainter  # For painting the pdf content
from PyQt6.uic import loadUi  # Load UI files

class MyForm(QDialog):  # main class for the apl

    def __init__(self):  # sets up UI and button connections
        super().__init__()
        self.ui = loadUi('exam5_santana.ui', self)  # loads the UI from the file
        self.pushButtonCalc.clicked.connect(self.calcMethod)  # connects calc button
        self.pushButtonExit.clicked.connect(self.exitMethod)  # conects exit button
        self.pushButtonPDF.clicked.connect(self.printMethod)  # connects PDF button to print method

    def calcMethod(self):  # method to calculate distance
        speed, okPressed = QInputDialog.getInt(self, "Enter Speed", "Speed in MPH:")  # ask user for speed
        if not okPressed:  # if they didt press OK, return
            return

        hours, okPressed = QInputDialog.getInt(self, "Enter Hours", "Time in Hours:")  # adk for hours traveled
        if not okPressed:  # if they didnt press OK again, stop
            return

        self.listWidgetOut.clear()  # clear the output area

        # Add speed and hours to the output list
        self.listWidgetOut.addItem(f"Vehicle Speed: {speed} MPH")
        self.listWidgetOut.addItem(f"Time Traveled: {hours} Hours")
        self.listWidgetOut.addItem("")  # blank line
        self.listWidgetOut.addItem("Hours    Distance Traveled")  # heading line

        total_distance = 0  # total distance starts at zero

        for hour in range(1, hours + 1):  # loop for each hour
            distance = speed * hour  # calculate distance
            self.listWidgetOut.addItem(f"{hour}          {distance} miles")  # show distance for each hour

        total_distance = speed * hours  # final total distance
        self.listWidgetOut.addItem(f"Total Distance: {total_distance}")  # display total

    def exitMethod(self):  # exit method for closing the app
        print("End of Distance Traveled Project 3, Original Work of: Alexander Santana")  # farewell msg
        self.close()  # close the dialog

    def printMethod(self):  # method for printing to PDF
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if not file_name:  # if no file name chosen, return
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)  # setting up printer
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)  # format to PDF
        printer.setOutputFileName(file_name)  # save to file

        painter = QPainter()  # painter object to draw the content
        if not painter.begin(printer):  # if it can't start painting, error
            print("Failed to start painting on the printer.")
            return

        scale_factor = 15.0  # scale factor makes it bigger on pdf
        painter.scale(scale_factor, scale_factor)  # apply scale
        list_widget_pixmap = self.listWidgetOut.grab()  # capture list widget
        painter.drawPixmap(0, 0, list_widget_pixmap)  # paint it onto pdf
        painter.end()  # end painting

        print(f"PDF saved to {file_name}")  # confirm saving

if __name__ == "__main__":  # main part of the program
    app = QApplication(sys.argv)  # create app
    window = MyForm()  # create the window
    window.show()  # show the window
    sys.exit(app.exec())  # exit app when closed

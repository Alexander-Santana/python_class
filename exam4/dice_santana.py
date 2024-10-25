# import all the stuff we need for the program
import sys  # this is for exiting the app
from PyQt6.QtWidgets import QDialog, QApplication  # for making the window and stuff
from PyQt6.QtGui import QPixmap  # this is for showing dice
from PyQt6.uic import loadUi  # load the .ui file
from PyQt6.QtCore import QTimer, QDateTime, QLocale  # handle the clock and time things
from random import randint  # we need this to get random numbers for the dice
from time import sleep  # this is so we can pause in the middle of rolling dice

# make a class for the Dice Simulator window
class DiceSimulator(QDialog):
    def __init__(self):
        super().__init__()  # this calls the parent class's constructor
        loadUi('dice_santana.ui', self)  # load the ui from the filwe

        # set up a timer that will update the clock every second
        self.timer = QTimer(self)  # make a timer
        self.timer.timeout.connect(self.showLCD)  # when timer finishes, update clock
        self.timer.start(1000)  # starts ticking every 1000 ms (1 second)

        # connect the buttons to their functions
        self.pushButtonRoll.clicked.connect(self.rollMethod)  # roll button rolls dice
        self.pushButtonExit.clicked.connect(self.exitMethod)  # exit button quits the app

        # show starting images for the dice (both show the 6th side first)
        self.displayImage("Die6.BMP", self.labelDie1)  # dice 1 shows side 6
        self.displayImage("Die6.BMP", self.labelDie2)  # dice 2 shows side 6

    # this will update the clock on the screen (the LCD display)
    def showLCD(self):
        current_datetime = QDateTime.currentDateTime()  # get the current time
        current_time = current_datetime.toString("hh:mm:ss")  # format the time as hours:minutes:seconds
        self.lcdNumber.display(current_time)  # show the time on the lcd

    # this is what happens when the user clicks the roll button
    def rollMethod(self):
        # Immediately show the '6' face before rolling starts
        self.displayImage("Die6.BMP", self.labelDie1)  # show 6 on dice 1
        self.displayImage("Die6.BMP", self.labelDie2)  # show 6 on dice 2

        # Simulate the dice roll with a loop
        for i in range(6):  # Loop through all 6 dice faces
            self.displayImage(f"Die{i+1}.BMP", self.labelDie1)  # show sides 1 to 6 on dice 1
            self.displayImage(f"Die{i+1}.BMP", self.labelDie2)  # show sides 1 to 6 on dice 2
            QApplication.processEvents()  # Process events to ensure the GUI updates
            sleep(0.08)  # Add a small delay to simulate rolling

        # After rolling, show the final random dice roll
        die1 = randint(1, 6)  # pick a random number for dice 1
        die2 = randint(1, 6)  # pick a random number for dice 2
        self.displayImage(f"Die{die1}.BMP", self.labelDie1)  # show the random side on dice 1
        self.displayImage(f"Die{die2}.BMP", self.labelDie2)  # show the random side on dice 2

    # this function shows an image in the label
    def displayImage(self, filename, label):
        pixmap = QPixmap(filename)  # create a pixmap from the file (image)
        if not pixmap.isNull():  # Check if the image was loaded successfully
            label.setPixmap(pixmap.scaled(label.width(), label.height()))  # Scale image to fit the label
        else:
            print(f"Something went Horribly wrong")  # Error handling

    # this is what happens when the exit button is clicked
    def exitMethod(self):
        QApplication.instance().quit()  # this quits the whole app

# start the app
if __name__ == "__main__":
    app = QApplication(sys.argv)  # create the app object
    window = DiceSimulator()  # make a window for the dice simulator
    window.show()  # show the window
    sys.exit(app.exec())  # execute the app (keep it running)

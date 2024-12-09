from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QMutex
import os

# Define the pingRange class for scanning IP ranges
class pingRange(QObject):
    sendTextSignal = pyqtSignal(str)
    dataSignal = pyqtSignal(list)
    finishedSignal = pyqtSignal()

    def __init__(self, base_ip, start, end):
        super().__init__()
        self.base_ip = base_ip
        self.start = start
        self.end = end
        self.data = []

    def scanRange(self):
        for i in range(self.start, self.end + 1):
            ip = f"{self.base_ip}.{i}"
            response = os.system(f"ping -n 1 {ip} > nul 2>&1")  # Adjust for Windows; use "-c 1" for Linux/Mac
            result = f"{ip} is {'reachable' if response == 0 else 'unreachable'}\n"
            self.sendTextSignal.emit(result)
            if response == 0:  # Collect reachable IPs
                self.data.append(ip)
        self.dataSignal.emit(self.data)
        self.finishedSignal.emit()

# Define the main form class
class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('pingscan_santana.ui', self)  # Load the UI file

        # Connect buttons to their respective functions
        self.pushButtonRunScan1.clicked.connect(self.run_scan1)
        self.pushButtonRunScan2.clicked.connect(self.run_scan2)
        self.pushButtonSave.clicked.connect(self.save_results)

        # Initialize variables
        self.data = []
        self.data_lock = QMutex()  # To handle thread-safe data access

    def run_scan1(self):
        self.thread1 = QThread()
        self.obj1 = pingRange('192.168.1', 2, 10)  # Scan range 192.168.1.2 to 192.168.1.10
        self.obj1.moveToThread(self.thread1)

        # Connect signals for Scan 1
        self.obj1.sendTextSignal.connect(self.plainTextEditScan1.insertPlainText)
        self.obj1.dataSignal.connect(self.obtain_results1)
        self.obj1.finishedSignal.connect(self.thread1.quit)

        # Start the thread
        self.thread1.started.connect(self.obj1.scanRange)
        self.thread1.start()

    def run_scan2(self):
        self.thread2 = QThread()
        self.obj2 = pingRange('192.168.1', 11, 20)  # Scan range 192.168.1.11 to 192.168.1.20
        self.obj2.moveToThread(self.thread2)

        # Connect signals for Scan 2
        self.obj2.sendTextSignal.connect(self.plainTextEditScan2.insertPlainText)
        self.obj2.dataSignal.connect(self.obtain_results2)
        self.obj2.finishedSignal.connect(self.thread2.quit)

        # Start the thread
        self.thread2.started.connect(self.obj2.scanRange)
        self.thread2.start()

    def obtain_results1(self, data):
        self.data_lock.lock()
        self.data += data
        self.data_lock.unlock()

    def obtain_results2(self, data):
        self.data_lock.lock()
        self.data += data
        self.data_lock.unlock()

    def save_results(self):
        try:
            with open('scan_results.csv', 'w') as file:
                file.write("Reachable IPs:\n")
                for ip in self.data:
                    file.write(f"{ip}\n")
            self.statusbar.showMessage("Results saved to scan_results.csv", 5000)
        except Exception as e:
            self.statusbar.showMessage(f"Error saving results: {str(e)}", 5000)

# Main execution
if __name__ == "__main__":
    app = QApplication([])
    window = MyForm()
    window.show()
    app.exec()

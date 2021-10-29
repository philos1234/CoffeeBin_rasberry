import sys
import time
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtCore import *
import get_phone_number as phone
import error


main_ui = uic.loadUiType("main.ui")[0]



class MainWindow(QMainWindow, main_ui,QCoreApplication):
    done_signal = pyqtSignal()

    def signal_run(self):
        self.done_signal.emit()
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.img_label.setPixmap(QtGui.QPixmap("coffee.png"))
        self.img_label.setGeometry(QtCore.QRect(250,50,500,500))
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def show(self):
        super().show()

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()
  
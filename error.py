import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic,QtGui,QtCore

error_ui = uic.loadUiType("error.ui")[0]


class ErrorWindow(QMainWindow,error_ui):
    done_signal = pyqtSignal()

    def signal_run(self):
        self.done_signal.emit()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.img_label.setPixmap(QtGui.QPixmap("X.png"))
        self.img_label.setGeometry(QtCore.QRect(270,70,450,450))
        self.done_signal.connect(QCoreApplication.instance().quit)
        self.confirm.clicked.connect(self.btn_confirm)
        
    def btn_confirm(self):
        self.signal_run()

    def show(self):
        super().show()
       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = ErrorWindow()
    myWindow.show()
    app.exec_()
  
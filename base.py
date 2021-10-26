import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtCore import *
import get_phone_number as phone
import error



if __name__ == "__main__":
    app = QApplication(sys.argv)
    integer = int(input('입력'))
    if integer == 1:
        print("111")
        myWindow = phone.PhoneWindow() 
        myWindow.show()
        app.exec_()
        
    elif integer == 2:
        print("222")
        myWindow = error.ErrorWindow() 
        myWindow.show()
        app.exec_()
    
    print("done")
    
   
  
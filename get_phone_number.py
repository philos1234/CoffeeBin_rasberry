import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re

form_class =uic.loadUiType("get_phone_number.ui")[0]


class MyWindow(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.str = ""
        self.result_number = ""
        self.number_match = re.compile('\d{3}-\d{3,4}-\d{4}')
        self.setupUi(self)
        self.inputProcess()

    def inputProcess(self): 
                # 버튼
        self.one.clicked.connect(self.btn_one)
        self.two.clicked.connect(self.btn_two)
        self.three.clicked.connect(self.btn_three)
        self.four.clicked.connect(self.btn_four)
        self.five.clicked.connect(self.btn_five)
        self.six.clicked.connect(self.btn_six)
        self.seven.clicked.connect(self.btn_seven)
        self.eight.clicked.connect(self.btn_eight)
        self.nine.clicked.connect(self.btn_nine)
        self.zero.clicked.connect(self.btn_zero)
        self.confirm.clicked.connect(self.btn_confirm)
        self.reset.clicked.connect(self.btn_reset)
        self.sack_jae.clicked.connect(self.btn_del)
        self.dash.clicked.connect(self.btn_dash)

    def btn_one(self):
        self.display.setText(self.str+"1")
        self.str += "1"
        
    def btn_two(self):
        self.display.setText(self.str+"2")
        self.str += "2"
    def btn_three(self):
        self.display.setText(self.str+"3")
        self.str += "3"
    def btn_four(self):
        self.display.setText(self.str+"4")
        self.str += "4"       
    def btn_five(self):
        self.display.setText(self.str+"5")
        self.str += "5"
    def btn_six(self):
        self.display.setText(self.str+"6")
        self.str += "6"
    def btn_seven(self):
        self.display.setText(self.str+"7")
        self.str += "7"
    def btn_eight(self):
        self.display.setText(self.str+"8")
        self.str += "8"
    def btn_nine(self):
        self.display.setText(self.str+"9")
        self.str += "9"
    def btn_zero(self):
        self.display.setText(self.str+"0")
        self.str += "0"

    def btn_confirm(self):
        if self.number_match.match(self.str) == None:
            self.display.setText("번호를 제대로 입력해주세요")
            return
        self.display.setText("적립 완료")
        self.result_number = self.str
        sys.exit(app.exec_())
    def btn_reset(self):
        self.display.clear()
        self.str = ""

    def btn_dash(self):
        self.display.setText(self.str+"-")
        self.str += "-"

    def btn_del(self):
        if len(self.str) == 0 : return
        self.str = self.str.rstrip(self.str[-1])
        self.display.setText(self.str)
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
  
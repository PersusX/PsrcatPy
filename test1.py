#!/Users/persusx/anaconda3/bin/python
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
  
  
class Window(QMainWindow):
    style = '''
#cSearchWeight{
    border:0px solid rgb(20,20,20);
    border-radius:15px;
    background-color:rgb(200,200,200);
}

#lineEdit{
    border:10px solid rgb(12,12,12);
    color:rgb(20,20,20);
    border-radius:15px;
    padding-left:50px;
    background-color:rgba(200,200,200,0);
    font-family:Roman times;
    font-size:16px;
}



#searchBtn{
    border:0;
    background-color:rgba(200,200,200,0); /*完全透明*/
    border-image:url(:/icon/Resource/search.png)
    
}

#searchBtn:hover{
    border:0;
    border-image:url(:/icon/Resource/searchhover.png)
}
    '''
    def __init__(self):
        super().__init__()
  
        # setting title
        self.setWindowTitle("Python ")
  
        # setting geometry
        self.setGeometry(100, 100, 600, 400)
  
        # calling method
        self.UiComponents()
  
        # showing all the widgets
        self.show()
  
    # method for widgets
    def UiComponents(self):
  
        # creating a combo box widget
        self.combo_box = QComboBox(self)
  
        # setting geometry of combo box
        self.combo_box.setGeometry(200, 150, 150, 30)
  
        # making combo box editable
        self.combo_box.setEditable(True)
  
        # geek list
        geek_list = ["Sayian", "Super Sayian", "Super Sayian 2", "Super Sayian B"]
  
        # adding list of items to combo box
        self.combo_box.addItems(geek_list)
  
        # creating line edit widget
        line_edit = QLineEdit()
  
        # setting background color to the line edit widget
          
        line_edit.setFrame(False)
        line_edit.setStyleSheet("background: qradialgradient(cx:0, cy:0, radius: 1,\
fx:0.5, fy:0.5, stop:0 white, stop:1 rgba(0,190,0, 60%));\
border-radius: 9px;")

        # adding line edit widget to combo box
        self.combo_box.setLineEdit(line_edit)
  
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
  
# start the app
sys.exit(App.exec())

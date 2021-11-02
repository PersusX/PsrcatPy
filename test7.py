#!/Users/persusx/anaconda3/bin/python
from PyQt5 import QtWidgets
from main_windows import Ui_MainWindow
import sys
from wid_defs import my_widgets
from dlg_defs import my_Dialog
 
class MyWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setupUi(self)
        
    def openDialog(self):
         self.dlg = my_Dialog()
         www = self.textEdit.toPlainText()
         self.dlg.setT(www)
         self.dlg.exec_()
        
    def openWidget(self):
        self.wid = my_widgets()
        self.wid.pushButton.clicked.connect(self.GetText)
        www= self.textEdit.toPlainText()
        self.wid.setT(www)
        self.wid.show() #close wid form
    def GetText(self):
        self.textEdit.setText(self.wid.textEdit.toPlainText())
        self.wid.close()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyWindow()
    mainWindow.show()
    sys.exit(app.exec_())

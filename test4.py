#!/Users/persusx/anaconda3/bin/python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
 
 
class Win_child(QDialog):
    # 自定义信号
    mySignal = pyqtSignal(str)
 
    def __init__(self, parent=None):
        super(Win_child, self).__init__(parent)
        self.initUI()
 
    def initUI(self):
        self.edit = QLineEdit(self)
 
 
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        write_btn = QPushButton('write', self)
        write_btn.clicked.connect(self.sendEditContent)
        concel_btn = QPushButton('concel', self)
        concel_btn.clicked.connect(self.close)
        hbox.addWidget(write_btn)
        hbox.addWidget(concel_btn)
 
        self.setWindowTitle('MyDialog')
        self.setGeometry(300, 300, 300, 200)
 
    def sendEditContent(self):
        content = self.edit.text()
        # 信号接收内容并传递
        self.mySignal.emit(content)
 
class Example(QWidget):
 
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
 
    def initUI(self):
 
        vbox = QVBoxLayout()
        self.setLayout(vbox)
 
        test_btn = QPushButton('open', self)
        test_btn.clicked.connect(self.get_content)
        self.test_label = QLabel("test", self)
 
        vbox.addWidget(test_btn)
        vbox.addWidget(self.test_label)
 
        self.setWindowTitle('test')
        self.show()
 
    def get_content(self):
        my = Win_child(self)
        # 槽接收信号
        my.mySignal.connect(self.setText)
        my.exec_()
 
    def setText(self, content):
        self.test_label.setText(content)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Example()
    form.show()
    sys.exit(app.exec_())
 

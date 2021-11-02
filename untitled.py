#!/Users/persusx/anaconda3/bin/python
from PyQt5 import QtCore, QtGui, QtWidgets
 
 
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1014, 701)
        self.myButton = QtWidgets.QPushButton(Form)
        self.myButton.setGeometry(QtCore.QRect(90, 450, 171, 81))
        self.myButton.setObjectName("myButton")
        self.tb = QtWidgets.QTextEdit(Form)
        self.tb.setGeometry(QtCore.QRect(80, 170, 531, 241))
        self.tb.setObjectName("tb")
        self.myButton_2 = QtWidgets.QPushButton(Form)
        self.myButton_2.setGeometry(QtCore.QRect(430, 450, 171, 81))
        self.myButton_2.setObjectName("myButton_2")
 
        self.retranslateUi(Form)
        self.myButton_2.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)
 
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

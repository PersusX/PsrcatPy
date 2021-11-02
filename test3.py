#!/Users/persusx/anaconda3/bin/python
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedLayout, QWidget,QToolBar, QToolButton, QStyle,  QColorDialog,  QFontDialog,QVBoxLayout, QGroupBox, QRadioButton)

class  DemoStackedLayout(QMainWindow):
    def __init__(self, parent=None):
        super(DemoStackedLayout, self).__init__(parent)

        # 设置窗口标题
        self.setWindowTitle('实战PyQt5: QStackedLayout Demo!')
        # 设置窗口大小
        self.resize(480, 360)

        self.initUi()
    def initUi(self):
        toolBar  =  QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, toolBar)
    
        btnColor = self.createButton('颜色对话框')
        btnColor.clicked.connect(lambda: self.onButtonClicked(0))
        toolBar.addWidget(btnColor)
        btnFont = self.createButton('字体对话框')
        btnFont.clicked.connect(lambda: self.onButtonClicked(1))
        toolBar.addWidget(btnFont)
        btnUser = self.createButton('分组部件')
        btnUser.clicked.connect(lambda: self.onButtonClicked(2))
        toolBar.addWidget(btnUser)
    
        mainWidget = QWidget(self)
 
        self.mainLayout = QStackedLayout(mainWidget)
    
        #添加三个widget,演示三个页面之间的切换
    
        # 颜色对话框
        self.mainLayout.addWidget(QColorDialog(self))
        #字体对话框
        self.mainLayout.addWidget(QFontDialog(self))
        #自定义控件
        self.mainLayout.addWidget(self.createExclusiveGroup())
    
        mainWidget.setLayout(self.mainLayout)
        #设置中心窗口
        self.setCentralWidget(mainWidget)
    
    
    def createButton(self, text):
        icon = QApplication.style().standardIcon(QStyle.SP_DesktopIcon)
        btn = QToolButton(self)
        btn.setText(text)
        btn.setIcon(icon)
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    
        return btn
  
    def onButtonClicked(self, index):
        if index < self.mainLayout.count():
            self.mainLayout.setCurrentIndex(index)
    
    def createExclusiveGroup(self):
        groupBox = QGroupBox('Exclusive Radio Buttons', self)
    
        radio1 = QRadioButton('&Radio Button 1', self)
        radio1.setChecked(True)
        radio2 = QRadioButton('R&adio button 2', self)
        radio3 = QRadioButton('Ra&dio button 3', self)
    
        vLayout = QVBoxLayout(groupBox)
        vLayout.addWidget(radio1)
        vLayout.addWidget(radio2)
        vLayout.addWidget(radio3)
        vLayout.addStretch(1)
    
        groupBox.setLayout(vLayout)
    
        return groupBox
  
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = DemoStackedLayout()
  window.show()
  sys.exit(app.exec())


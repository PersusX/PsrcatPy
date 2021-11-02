# -*- coding: utf-8 -*-

"""
Created on 2021/5/1 12:30
@author: Persus & Xie
@email: Persusxie@outlook.com
@description: 
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Psrcat import psrcat



class PsrParaListItem(QWidget):
    style = '''
#btn_more{
    background-color:rgba(0,0,0,0);
    color:#404040;
}
#btn_more:hover{
    color:#707070;
}
    '''
    def __init__(self, parent=None,titleName='Pulsar',row=2, col=6,num=12,paralist=["pulsar"]*12):
        super(PsrParaListItem, self).__init__(parent)
        self.titleName = titleName
        self.col = col  # 每一行有多少列
        self.row = row
        self.num = num  ##一共多少个 其值大于 col*(row-1) 小于 col*row
        self.paralist = paralist ## checkbox name列表
        self.setupUi()

    def setupUi(self):
        #self.setMaximumWidth(1300)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.hly_title = QHBoxLayout()
        self.hly_title.setContentsMargins(0, 0, 0, 0)
        self.lb_title = QLabel(self.titleName)
        font = QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName("lb_title")
        self.lb_title.setFixedHeight(50)
        #self.btn_more = QPushButton('更多》')
        #self.btn_more.setObjectName('btn_more')
        self.hly_title.addWidget(self.lb_title)
        #spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #self.hly_title.addItem(spacerItem)
        #self.hly_title.addWidget(self.btn_more)
        self.main_layout.addLayout(self.hly_title)
        ## 设置线条
        self.line = QFrame(self)
        self.line.setMinimumSize(QSize(0, 1))
        self.line.setMaximumSize(QSize(1677721500, 1))
        self.line.setStyleSheet("border:1px solid #e5e5e5;")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.main_layout.addWidget(self.line)
        
        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(0, 20, 0, 20)
        #self.gridLayout.setSpacing(0)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        
        self.psrParaList = QListWidget()
        self.psrParaList.setObjectName('psrParaList')
        
        self.checkboxInfo_list = []
        
        
        
        for i in range(self.row):  # 默认两行
            if i != self.row-1:
                if i ==0:
                    for j in range(self.col):
                        psr_checkbox = QtWidgets.QCheckBox(self.paralist[(i+1)*(j+1)-1])
                        psr_checkbox.setObjectName('psr_checkbox')
                        self.vly = QVBoxLayout()
                        self.vly.setContentsMargins(0, 0, 0, 0)
                        self.vly.addWidget(psr_checkbox)
                        self.gridLayout.addLayout(self.vly, i, j)
                        self.checkboxInfo_list.append(psr_checkbox)
                else:
                    for j in range(self.col):
                        psr_checkbox = QtWidgets.QCheckBox(self.paralist[i*self.col+j])
                        psr_checkbox.setObjectName('psr_checkbox')
                        self.vly = QVBoxLayout()
                        self.vly.setContentsMargins(0, 0, 0, 0)
                        self.vly.addWidget(psr_checkbox)
                        self.gridLayout.addLayout(self.vly, i, j)
                        self.checkboxInfo_list.append(psr_checkbox)
                
            elif self.num%self.col !=0:
                for j in range(self.num%self.col):
                        psr_checkbox = QtWidgets.QCheckBox(self.paralist[i*self.col+j])
                        psr_checkbox.setObjectName('psr_checkbox')
                        self.vly = QVBoxLayout()
                        self.vly.setContentsMargins(0, 0, 0, 0)
                        self.vly.addWidget(psr_checkbox)
                        self.gridLayout.addLayout(self.vly, i, j)
                        self.checkboxInfo_list.append(psr_checkbox)
            else:
                for j in range(self.col):
                        psr_checkbox = QtWidgets.QCheckBox(self.paralist[i*self.col+j])
                        psr_checkbox.setObjectName('psr_checkbox')
                        self.vly = QVBoxLayout()
                        self.vly.setContentsMargins(0, 0, 0, 0)
                        self.vly.addWidget(psr_checkbox)
                        self.gridLayout.addLayout(self.vly, i, j)
                        self.checkboxInfo_list.append(psr_checkbox)


        self.main_layout.addLayout(self.gridLayout)
        #spacerItem = QSpacerItem(0, 0, 0, 0)
        #self.main_layout.addItem(spacerItem)

        self.setStyleSheet(self.style)

    def hideTitle(self):
        self.lb_title.hide()
        self.btn_more.hide()

   


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CcheckboxListWidget()
    # w.hideTitle()
    w.show()
    sys.exit(app.exec_())


#!/Users/persusx/anaconda3/bin/python

# code:utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import time


class MyTable(QTableWidget):
    def __init__(self, parent=None):
        super(MyTable, self).__init__()
        self.creatMessageline()
        mainLayout = QVBoxLayout()
        hboxLayout = QHBoxLayout()
        hboxLayout.addStretch()
        # hboxLayout.addWidget()#横向添加模块
        mainLayout.addLayout(hboxLayout)
        mainLayout.addWidget(self.Messageline)#纵向添加模块
        self.setLayout(mainLayout)
        self.setWindowTitle('测试')
    def creatMessageline(self):
        self.recv_id=["simple"]
        self.test_data = ["simple"]
        self.Messageline = QGroupBox("信息：")
        layout = QFormLayout()
        #testitemLabel = QLabel("测试：")
        #testitemEditor = QLabel(self.testitemInformation)
        #testitemEditor.setFont(QFont("Roman times",10,QFont.Bold))
        #pe = QPalette()#样式设置
        #pe.setColor(QPalette.WindowText, Qt.red)  # 设置字体颜色
        #testitemEditor.setPalette(pe)
        self.table = QTableWidget(99,3)
        self.table.setHorizontalHeaderLabels(["编号","测试","人员"])
        for i in range(len(self.recv_id)):
            self.table.setItem(i,0,QTableWidgetItem(str(self.recv_id[i])))
            self.table.setItem(i,1,QTableWidgetItem(str(self.test_data[i])))
            self.table.setItem(i,2,QTableWidgetItem("auto"))
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        #layout.addRow(testitemLabel,testitemEditor)
        layout.addRow(self.table)
        self.Messageline.setLayout(layout)

if __name__ == '__main__':
    # 实例化表格
    app = QApplication(sys.argv)
    myTable = MyTable()
    # 启动更新线程
    # 显示表格
    myTable.show()
    app.exit(app.exec_())

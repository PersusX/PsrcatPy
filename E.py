#!/Users/persusx/anaconda3/bin/python

#coding:utf-8

# 导入matplotlib模块并使用Qt5Agg
import matplotlib
matplotlib.use('Qt5Agg')
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import sys
import numpy as np
from numpy import *

class App(QtWidgets.QDialog):
    def __init__(self,parent=None):
        # 父类初始化方法
        super(App,self).__init__(parent)
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('PyQt5结合Matplotlib绘制函数图像')
        # 几个QWidgets
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.button_plot = QtWidgets.QPushButton("绘制函数图像")
        self.line = QLineEdit() # 输入函数
        # 连接事件
        self.button_plot.clicked.connect(self.plot_)
        
        # 设置布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.line)
        layout.addWidget(self.button_plot)
        self.setLayout(layout)

    # 连接的绘制的方法
    def plot_(self):
        ax = self.figure.add_axes([0.1,0.1,0.8,0.8])
        ax.clear() #每次绘制一个函数时清空绘图
        x = linspace(-3,3,6000)
        y = eval(self.line.text()) #使用了eval函数
        ax.plot(x,y)
        self.canvas.draw()

# 运行程序
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = App()
    main_window.show()
    app.exec()


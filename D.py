#!/Users/persusx/anaconda3/bin/python

# -*- coding: utf-8 -*-

"""
Module: plot data realtime.
Created on 2020/07/12 by Blog Author VERtiCaL at SSRF
"""
import sys
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # pyqt5的画布
import numpy as np
import matplotlib.pyplot as plt
# matplotlib.figure 模块提供了顶层的Artist(图中的所有可见元素都是Artist的子类)，它包含了所有的plot元素
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets



class MyMatplotlibFigure(FigureCanvasQTAgg):
    """
    创建一个画布类，并把画布放到FigureCanvasQTAgg
    """
    def __init__(self, width=10, heigh=10, dpi=100):
        plt.rcParams['figure.facecolor'] = 'w'  # 设置窗体颜色
        plt.rcParams['axes.facecolor'] = 'w'  # 设置绘图区颜色
        # 创建一个Figure,该Figure为matplotlib下的Figure，不是matplotlib.pyplot下面的Figure
        self.figs = Figure(figsize=(width, heigh), dpi=dpi)
        super(MyMatplotlibFigure, self).__init__(self.figs)  # 在父类种激活self.fig，
        self.axes = self.figs.add_subplot(111)  # 添加绘图区
    def mat_plot_drow_axes(self, t, s):
        """
        用清除画布刷新的方法绘图
        :return:
        """
        self.axes.cla()  # 清除绘图区

        #self.axes.spines['top'].set_visible(False)  # 顶边界不可见
        #self.axes.spines['right'].set_visible(False)  # 右边界不可见
        self.axes.spines['top'].set_visible(True)  # 顶边界不可见
        self.axes.spines['right'].set_visible(True)  # 右边界不可见
        # 设置左、下边界在（0，0）处相交
        # self.axes.spines['bottom'].set_position(('data', 0))  # 设置y轴线原点数据为 0
        self.axes.spines['left'].set_position(('data', 0))  # 设置x轴线原点数据为 0
        self.axes.plot(t, s, 'o-k', linewidth=0.5)
        self.figs.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.figs.canvas.flush_events()  # 画布刷新self.figs.canvas

class MainDialogImgBW(QtWidgets.QMainWindow):
    """
    创建UI主窗口，使用画板类绘图。
    """
    def __init__(self):
        super(MainDialogImgBW, self).__init__()
        self.setWindowTitle("显示matplotlib")
        self.setObjectName("widget")
        self.resize(800, 600)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.canvas = MyMatplotlibFigure(width=5, heigh=4, dpi=100)
        self.plotcos()
        self.hboxlayout = QtWidgets.QHBoxLayout(self.label)
        self.hboxlayout.addWidget(self.canvas)

    def plotcos(self):
        # plt.clf()
        t = np.arange(0.0, 5.0, 0.01)
        s = np.cos(2 * np.pi * t)
        self.canvas.mat_plot_drow_axes(t, s)
        self.canvas.figs.suptitle("sin")  # 设置标题


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainDialogImgBW()
    main.show()
    sys.exit(app.exec_())


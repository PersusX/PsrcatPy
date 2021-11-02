#!/Users/persusx/anaconda3/bin/python
# version 1.1
# this sopftware is to get the value and parameter of psrcat.db
# Contact PersusXie@outlook.com if in doubt


from Gui.MainWindow import Ui_MainWindow
from CommanHelper.FileHelper import *
from Contral.LeftNavigation import *
from Contral.Playing import *
from Contral.DM.DM import *
from Contral.FindMusic.FindMusic import *
from Contral.PopWindow.PlayingTable import *
from Contral.PopWindow.MyOperation import *
from CustomWidgets.CSearchEdit import *
from CustomWidgets.CicularLabel import *
from Gui.FindMusicUi.RecommandUi.Ui_Recommand import *

class MyWin(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setupUi(self)
        self.initMainWinUi()
        self.initHeadUi()
        self.initBodyUi()
        
        self.initBottomUi()

    def initMainWinUi(self):
        self.centralwidget.setAttribute(Qt.WA_TranslucentBackground)
        self.showMainWinShadow()


    def initHeadUi(self):
        '''变量'''
        self.isMaxWin = False  # 窗口是否已经最大化
        self.isSignin = True  # 是否已经登录
        self.isOpenMyOpt = False  # 登录后是否打开了myOperation
        '''控件'''
        self.le_searchPulsar = CSearchEdit('search a pulsar', 300)
        self.hly_search.addWidget(self.le_searchPulsar)
        self.myOperation = MyOperation()
        self.btn_userImage = CCircularLabel(self, 30)
        self.btn_userImage.setPixmap(QPixmap(':/pic/Resource/userimage.jpg'))
        self.vly_userimage.addWidget(self.btn_userImage)

        '''绑定槽函数'''
        self.btn_maxwin.clicked.connect(self.showMaxNormalWin)
        self.btn_signin.clicked.connect(self.btnSignin)

    def initBodyUi(self):
        '''变量'''

        '''控件'''
        self.leftNavigation = LeftNavigation(self)
        self.vly_leftBar.addWidget(self.leftNavigation)
        ## pulsar parameter 页面绑定
        self.findMusic = FindMusic()
        self.hly_findMusic.addWidget(self.findMusic)
        self.pushButton.clicked.connect(lambda ite: self.findMusic.tab_pulsar_para.setCurrentIndex(0))
       
        
        
        ## dm页面绑定
        self.dm = DM()
        self.hly_dm.addWidget(self.dm)
        '''绑定槽函数'''
        #if self.lw_recommand.currentRowIndex == 0:
        #    self.body_stackedWidget.setCurrentIndex(1)
        #else:
        ### 设置堆叠页面转换
        #self.body_stackedWidget.setCurrentIndex(1)
        self.leftNavigation.lw_recommand.itemClicked.connect(lambda ite: print("kukuku",int(ite.whatsThis())))
        self.leftNavigation.lw_recommand.itemClicked.connect(lambda ite: self.body_stackedWidget.setCurrentIndex(int(ite.whatsThis())-1))
        #self.UiRecommand =  UiRecommand(self)
        
        #self.btn_table.clicked.connect(lambda ite: self.body_stackedWidget.setCurrentIndex(1))
        #self.leftNavigation.get_itemindex()
    #def changeUi(self):


    def initBottomUi(self):
        '''变量'''
        self.playOrder = 0  # 当前播放顺序默认为顺序播放
        '''控件'''
        #self.playing = PlayingWidget()
        #self.vly_leftBar.addWidget(self.playing)

        self.isPlayListOpen = False  # 默认播放列表没有打开
        self.playList = PlayingTable(parentHeight=self.height())
        self.playList.setParent(self.centralwidget)
        self.playList.close()
        '''绑定槽函数'''
        self.btn_playList.clicked.connect(self.btnOpenOrClosePlayList)
        #self.btn_playOder.clicked.connect(self.btnChangePlayOrder)

    def mousePressEvent(self, a0: QMouseEvent):
        # 鼠标不在播放列表控件内，点击鼠标就会关闭播放列表
        if not self.playList.geometry().contains(self.mapFromGlobal(QCursor.pos())):
            self.playList.close()
            self.isPlayListOpen = False
        # 鼠标不在myOperation控件内，点击鼠标就会关闭
        # if
    ### 设置窗口可移动: mousePressEvent,mouseMoveEvent,mouseReleaseEvent
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            #self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def resizeEvent(self, a0: QResizeEvent):
        # 如果播放列表显示了，则同步更变播放列表的位置
        self.playList.setFixedHeight(int(0.7*self.height()))
        self.playList.move(self.centralwidget.width() - self.playList.width(),
                           self.centralwidget.height() - (self.playList.height() + self.broadcast_widget.height()))
        # “我的操作”页面也要随窗口大小变化而变化
        x = self.btn_signin.x() + int(self.btn_signin.width() / 2) - int(self.myOperation.width() / 2)
        y = self.head_widget.height() - 10
        self.myOperation.move(x, y)

    def showMaximized(self):
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        super(MyWin, self).showMaximized()

    def showNormal(self):
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.showMainWinShadow()
        super(MyWin, self).showNormal()

    def showMainWinShadow(self):
        # 实例阴影shadow
        self.shadow = QGraphicsDropShadowEffect(self.centralwidget)
        # 设置阴影距离
        self.shadow.setOffset(0, 0)
        # 设置阴影圆角
        self.shadow.setBlurRadius(19)
        # 设置阴影颜色
        self.shadow.setColor(Qt.black)
        self.setGraphicsEffect(self.shadow)

    '''******************************header的槽函数*****************************'''
    def showMaxNormalWin(self):
        if self.isMaxWin:
            self.showNormal()
            qss = '''
            #btn_maxwin{
                border-image:url(:/icon/Resource/maxwin.png);
            }
            #btn_maxwin:hover{
                border-image:url(:/icon/Resource/maxwin1.png);
            }
            '''
            self.btn_maxwin.setStyleSheet(qss)
        else:
            qss = '''
                #btn_maxwin{
                    border-image:url(:/icon/Resource/winret.png);
                }
                #btn_maxwin:hover{
                    border-image:url(:/icon/Resource/winret1.png);
                }
                '''
            self.btn_maxwin.setStyleSheet(qss)
            self.showMaximized()
        self.isMaxWin = not self.isMaxWin

    def btnSignin(self):
        if self.isSignin == True:  # 已经登录就显示我的操作页面
            if self.isOpenMyOpt == False:
                self.myOperation.setParent(self)
                x = self.btn_signin.x() + int(self.btn_signin.width() / 2) - int(self.myOperation.width()/2)
                y = self.head_widget.height() - 10
                self.myOperation.move(x, y)
                self.myOperation.show()
            else:
                self.myOperation.close()
            self.isOpenMyOpt = not self.isOpenMyOpt
        else:
            pass

    '''*************************bottom的槽函数***********************'''
    def btnOpenOrClosePlayList(self):
        '''点击播放列表，打开或关闭列表'''
        if self.isPlayListOpen:
            self.isPlayListOpen = not self.isPlayListOpen
            self.playList.close()
        else:
            self.isPlayListOpen = not self.isPlayListOpen
            self.playList.setParent(self.centralwidget)
            self.playList.move(self.centralwidget.width()-self.playList.width(), self.centralwidget.height()-(self.playList.height()+self.broadcast_widget.height()))
            self.playList.show()

    def btnChangePlayOrder(self):
        self.playOrder = self.playOrder + 1
        if self.playOrder > 3:
            self.playOrder = 0
        icon_list = ['sequenceplay.png', 'table.png','randomplay.png', 'loopplay.png', 'loopone.png']
        icon_list1 = ['sequenceplay1.png', 'table1.png','randomplay1.png', 'loopplay1.png', 'loopone1.png']
        qss = '#btn_playOder{' \
                    'border-image:url(:/icon/Resource/' + icon_list[self.playOrder] + ');' \
                '}' \
                '#btn_playOder:hover{' \
                     'border-image:url(:/icon/Resource/' +icon_list1[self.playOrder] + ');' \
                 '}'
        self.btn_playOder.setStyleSheet(qss)

    '''*****************************************其他函数***************************************'''



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    stylefile = './style.qss'
    qssStyle = FlieHelper.readQss(stylefile)
    myWin = MyWin()
    myWin.setStyleSheet(qssStyle)
    myWin.show()
    sys.exit(app.exec_())
